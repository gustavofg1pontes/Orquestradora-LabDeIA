import datetime
import os
import bcrypt
from flask import jsonify
import jwt
from config.db import collection_config
from models.User import User

secret = os.getenv("SECRET")

class AuthService:
  def __init__(self, collection_name):
    self.collection = collection_config(collection_name)

  def register(self, name, email, senha):
    if self.collection.count_documents({"email": email}) > 0:
      return jsonify({"error": "Endereço de e-mail já cadastrado"}), 400
    
    senha = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    user = User(None, email, senha, name)

    self.collection.insert_one(user.to_dict())
    return jsonify({"message": "Usuário cadastrado com sucesso"}), 201
  
  def login(self, email, senha):
    user = self.collection.find_one({"email": email})
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