from flask import Flask
from web.extensions import db, login_manager, alembic, socketio
from web.models import Player


@login_manager.user_loader
def load_user(user_id):
    return db.session.execute(
        db.select(Player).filter_by(id=user_id)).scalar()


def create_app(debug=False):
    """Create an application."""
    app = Flask(__name__)
    app.config.from_object('web.settings.config.Config')

    from web.routes import routes
    app.register_blueprint(routes)
    register_extensions(app)

    return app


def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    alembic.init_app(app)
    socketio.init_app(app)
