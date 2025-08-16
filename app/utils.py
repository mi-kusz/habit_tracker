from datetime import datetime, timezone

from flask import Response, jsonify


def get_utc_time() -> datetime:
    return datetime.now(timezone.utc)


def create_error_response(message: str) -> Response:
    return jsonify({"error": message})