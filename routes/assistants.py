from flask import request, jsonify
from flask import Blueprint

from services.AssistantService import AssistantService
from utils.tokendec import token_required

assistants_app = Blueprint('assistants_app', __name__)

assistantService = AssistantService()

@assistants_app.route("/assistants/add", methods=['POST'])
@token_required
def add_assistant():
    response_insert = assistantService.insert_one(request.json)
    
    response_data = {"id": str(response_insert["id"]), "api_key": str(response_insert["api_key"])}
    response = jsonify(response_data)
    response.status_code = 201
    response.headers["Location"] = f"/assistants/get/{response_insert['id']}"
    response.content_type = "application/json"
    
    return response


@assistants_app.route("/assistants/list", methods=['GET'])
@token_required
def get_assistants():
    return assistantService.list()


@assistants_app.route("/assistants/get/<id>", methods=['GET'])
@token_required
def get_assistant(id):
    return assistantService.get(id)


@assistants_app.route("/assistants/update/<id>", methods=['PUT'])
@token_required
def update_assistant(id):
    return assistantService.update(id, request.json)


@assistants_app.route("/assistants/delete/<id>", methods=['DELETE'])
@token_required
def delete_assistant(id):
    return assistantService.delete(id)
