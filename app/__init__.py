from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from config import DATABASE_PATH

database: SQLAlchemy = SQLAlchemy()


def init_database(app: Flask) -> None:
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        DATABASE_PATH
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    database.init_app(app)


def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)

    from .routes.user_routes import user_blueprint

    app.register_blueprint(user_blueprint, url_prefix="/users")

    init_database(app)

    from .models import Category, ExecutionHistory, HabitTask, User

    with app.app_context():
        database.create_all()

    return app