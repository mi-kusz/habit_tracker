from http import HTTPStatus
from typing import Optional

from flask import Blueprint, jsonify, request

from app.exceptions.exceptions import MissingAuthData, InvalidCredentials
from app.exceptions.handlers import create_error_response
from ..services import auth_service

auth_blueprint = Blueprint("auth", __name__)

@auth_blueprint.route("/login", methods=["POST"])
def login():
    try:
        payload: Optional[dict] = request.get_json()

        if payload is None:
            return create_error_response("Missing JSON body"), HTTPStatus.BAD_REQUEST

        email: Optional[str] = payload.get("email")
        password: Optional[str] = payload.get("password")

        token: str = auth_service.login(email, password)

        return jsonify({"access_token": token}), HTTPStatus.OK
    except (MissingAuthData, InvalidCredentials) as e:
        return create_error_response(str(e)), HTTPStatus.BAD_REQUEST