from http import HTTPStatus

from flask import Flask, Response, jsonify
from pydantic import ValidationError

from app.exceptions.exceptions import EntityNotFoundException, EntityPersistenceException, MissingAuthData, \
    InvalidCredentials


def create_error_response(message: str) -> Response:
    return jsonify({"error": message})


def register_handlers(app: Flask) -> None:
    @app.errorhandler(EntityNotFoundException)
    def handle_entity_not_found_error(e: EntityNotFoundException) -> tuple[Response, HTTPStatus]:
        return create_error_response(str(e)), HTTPStatus.NOT_FOUND

    @app.errorhandler(EntityPersistenceException)
    def handle_entity_persistence_error(e: EntityPersistenceException) -> tuple[Response, HTTPStatus]:
        return create_error_response(str(e)), HTTPStatus.BAD_REQUEST

    @app.errorhandler(PermissionError)
    def handle_permission_error(e: PermissionError) -> tuple[Response, HTTPStatus]:
        return create_error_response(str(e)), HTTPStatus.FORBIDDEN

    @app.errorhandler(ValueError)
    def handle_value_error(e: ValueError) -> tuple[Response, HTTPStatus]:
        return create_error_response(str(e)), HTTPStatus.BAD_REQUEST

    @app.errorhandler(ValidationError)
    def handle_validation_error(e: ValidationError) -> tuple[Response, HTTPStatus]:
        return create_error_response(str(e.errors())), HTTPStatus.BAD_REQUEST

    @app.errorhandler(MissingAuthData)
    def handle_missing_auth_data_error(e: MissingAuthData) -> tuple[Response, HTTPStatus]:
        return create_error_response(str(e)), HTTPStatus.BAD_REQUEST

    @app.errorhandler(InvalidCredentials)
    def handle_invalid_credentials_error(e: InvalidCredentials) -> tuple[Response, HTTPStatus]:
        return create_error_response(str(e)), HTTPStatus.BAD_REQUEST