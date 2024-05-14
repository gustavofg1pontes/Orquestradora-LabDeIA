import datetime
import os
import bcrypt
from flask import jsonify
import jwt
from models.User import User
from repositories.AuthRepository import AuthRepository

secret = os.getenv("SECRET")


class AuthService:
    def __init__(self):
        self.authRepository = AuthRepository()

    def register(self, name, email, senha):
        if self.authRepository.existsByEmail(email):
            return jsonify({"error": "Endereço de e-mail já cadastrado"}), 400

        senha = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user = User(None, email, senha, name)

        self.authRepository.insert(user.to_dict())
        return jsonify({"message": "Usuário cadastrado com sucesso"}), 201

    def login(self, email, senha):
        user = self.authRepository.findByEmail(email)
        if user:
            if bcrypt.checkpw(senha.encode('utf-8'), user["password"].encode('utf-8')):
                fuso_horario_brasileiro = datetime.timedelta(hours=-3)
                iat = datetime.datetime.now(tz=datetime.timezone.utc) + fuso_horario_brasileiro
                payload = {"id": str(user["_id"]), "admin": True, "iat": iat, "exp": iat + datetime.timedelta(days=3)}
                jwt_token = jwt.encode(payload, secret, algorithm="HS256")
                return jsonify({
                    "token": jwt_token,
                    "user": {
                        "id": str(user["_id"]),
                        "email": user["email"],
                        "name": user["name"]
                    }
                }), 200
            else:
                return jsonify({"error": "Senha incorreta"}), 401
        else:
            return jsonify({"error": "Usuário não encontrado"}), 404
