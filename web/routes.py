from flask import Blueprint, abort, redirect, render_template, request, flash
from flask_login import current_user, login_required, login_user, logout_user
from web.extensions import db
from passlib.hash import sha256_crypt
from web.models import Game, Session, Player
from web.utils import add_credits

routes = Blueprint("routes", __name__)


@routes.route('/home', methods=["GET", "POST"])
def home():
    if request.method == 'GET':
        if current_user.is_authenticated:
            return render_template("start.html", credits=current_user.credits)
        return render_template("start.html")
    if request.method == 'POST':
        if current_user.is_authenticated:
            add_credits(current_user)
            return render_template("start.html", credits=current_user.credits)
        return render_template("start.html")


@routes.route("/room", methods=["POST"])
@login_required
def room():
    code = request.form['code']

    game = db.session.execute(
        db.select(Game).filter_by(room_code=code, finished=False, in_progress=False)).scalar()

    if game is None:
        user_session = Session(player_id=current_user.id)
        game = Game(session=user_session, room_code=code)
    else:
        user_session = game.session

    db.session.add(game)
    db.session.commit()

    return render_template("room.html", code=code, session_id=user_session.id, game_id=game.id)


@routes.route('/', methods=['GET', 'POST'])
def login():
    """Function log in user to the game app if he already has an account. Otherwise it creates a new account."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        player = db.session.execute(
            db.select(Player).filter_by(username=username)).scalar()

        if player is not None:
            if sha256_crypt.verify(password, player.password):
                flash('Logged in successfully.')
            else:
                return abort(401, description="Invalid password")
        else:
            hash_password = sha256_crypt.encrypt(password)
            player = Player(username=username, password=hash_password)
            db.session.add(player)
            db.session.commit()

        login_user(player)
        return redirect("/home")
    return render_template("login.html")


@routes.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')
