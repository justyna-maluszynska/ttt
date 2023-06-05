from flask import Flask, abort, redirect, render_template, request, flash
from extensions import db, login_manager, alembic, socketio
from flask_login import login_required, login_user, logout_user
from passlib.hash import sha256_crypt
from models import Player


app = Flask(__name__)
app.config.from_object('settings.config.Config')

db.init_app(app)
login_manager.init_app(app)
alembic.init_app(app)
socketio.init_app(app)


@app.route('/', methods=["GET"])
def home():
    return render_template("home.html")


@login_manager.user_loader
def load_user(user_id):
    return db.session.execute(
        db.select(Player).filter_by(id=user_id)).scalar()


@app.route('/', methods=['GET', 'POST'])
def login():
    """Function log in user to the game app if he already has an account. Otherwise it creates a new account."""
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
    return redirect("/")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')


if __name__ == '__main__':
    socketio.run(app)
