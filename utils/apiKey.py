import secrets
import base64
from functools import wraps

from flask import request, jsonify

from config.assistant import AssistantConfig


def generate_key():
    token_bytes = secrets.token_bytes(96)
    token_base64 = base64.urlsafe_b64encode(token_bytes)[:64].decode('utf-8')
    return token_base64


# Decorator to require an API key
def api_key_required(route_function):
    @wraps(route_function)
    def wrapper(*args, **kwargs):
        api_key_header = request.headers.get('X-API-Key')

        if not api_key_header:
            return jsonify({"message": "X-API-Key header is required"}), 401

        return route_function(*args, **kwargs)

    return wrapper
