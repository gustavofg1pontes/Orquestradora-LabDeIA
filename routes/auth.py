from flask import request
from flask import Blueprint

from services.AuthService import AuthService

auth_service = AuthService("users")
auth_api = Blueprint('auth_api', __name__)

@auth_api.route('/auth/register', methods=['POST'])
def register():
    data = request.json
    return auth_service.register(data["name"], data["email"], data["password"])
  
@auth_api.route('/auth/login', methods=['POST'])
def login():
    data = request.json
    return auth_service.login(data["email"], data["password"])