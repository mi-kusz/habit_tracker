from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

from app.config import DATABASE_PATH
from app.exceptions.handlers import register_handlers

database: SQLAlchemy = SQLAlchemy()
jwt: JWTManager = JWTManager()


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
    from .routes.category_routes import category_blueprint
    from .routes.habit_task_routes import habit_task_blueprint
    from .routes.execution_history_routes import execution_history_blueprint
    from .routes.auth_route import auth_blueprint

    app.register_blueprint(user_blueprint, url_prefix="/users")
    app.register_blueprint(category_blueprint, url_prefix="/categories")
    app.register_blueprint(habit_task_blueprint, url_prefix="/habit_tasks")
    app.register_blueprint(execution_history_blueprint, url_prefix="/execution_histories")
    app.register_blueprint(auth_blueprint, url_prefix="/auth")

    init_database(app)

    from .models import Category, ExecutionHistory, HabitTask, User

    with app.app_context():
        database.create_all()

    app.config["JWT_SECRET_KEY"] = "secret-key"

    jwt.init_app(app)

    register_handlers(app)

    return app