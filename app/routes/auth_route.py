from http import HTTPStatus
from typing import Optional

from flask import Blueprint, jsonify

from ..services import auth_service
from ..utils import get_payload

auth_blueprint = Blueprint("auth", __name__)

@auth_blueprint.route("/login", methods=["POST"])
def login():
    payload: dict = get_payload()

    email: Optional[str] = payload.get("email")
    password: Optional[str] = payload.get("password")

    token: str = auth_service.login(email, password)

    return jsonify({"access_token": token}), HTTPStatus.OK