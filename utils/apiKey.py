import secrets
import base64

tokens_file = '../tokens.txt'


def generate_token():
    token_bytes = secrets.token_bytes(96)
    token_base64 = base64.urlsafe_b64encode(token_bytes)[:64].decode('utf-8')
    return token_base64


def generate_and_save_token(assistant_id):
    token = generate_token()
    with open(tokens_file, 'w') as file:
        file.write(f'{assistant_id}/{token}\n')
