from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_alembic import Alembic

login_manager = LoginManager()
db = SQLAlchemy()
alembic = Alembic()
socketio = SocketIO()
