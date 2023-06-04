from flask import Flask, render_template
import os
from extensions import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")


def register_extensions():
    """Register extensions used in a flask application"""
    db.init_app(app)
    # socketio.init_app(app)


@app.route('/', methods=["GET"])
def home():
    return render_template("home.html")
