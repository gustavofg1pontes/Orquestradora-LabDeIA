import secrets
import base64
from functools import wraps

from flask import request, jsonify

from config.assistant import AssistantConfig

tokens_file = './tokens.txt'


def generate_key():
    token_bytes = secrets.token_bytes(96)
    token_base64 = base64.urlsafe_b64encode(token_bytes)[:64].decode('utf-8')
    return token_base64


def generate_and_save_key(assistant_id):
    token = generate_key()
    with open(tokens_file, 'a') as file:
        file.write(f'{assistant_id}\n{token}\n\n')
    return token


def find_key(key):
    with open(tokens_file, 'r') as file:
        lines = file.readlines()
        for i in range(0, len(lines), 3):
            assistant_id = lines[i].strip()
            token = lines[i + 1].strip()
            if key == token:
                return assistant_id
    return None


# Decorator to require an API key
def api_key_required(route_function):
    @wraps(route_function)
    def wrapper(*args, **kwargs):
        api_key_header = request.headers.get('X-API-Key')

        if not api_key_header:
            return jsonify({"message": "X-API-Key header is required"}), 401

        assistant_id = find_key(api_key_header)
        if not assistant_id:
            return jsonify({"message": "Invalid X-API-Key"}), 401

        AssistantConfig.set_assistant_id(assistant_id)
        return route_function(*args, **kwargs)

    return wrapper
