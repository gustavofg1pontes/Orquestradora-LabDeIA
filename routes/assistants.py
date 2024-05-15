from flask import request, jsonify
from flask import Blueprint
from config.db import collection_config
from services.AssistantService import AssistantService

assistants_app = Blueprint('assistants_app', __name__)
collection = collection_config("assistants")
assistantService = AssistantService()

@assistants_app.route("/assistants/add", methods=['POST'])
def add_assistant():
    inserted_id = assistantService.insert_one(request)
    
    response_data = {"id": str(inserted_id)}
    response = jsonify(response_data)
    response.status_code = 201
    response.headers["Location"] = f"/assistants/get/{inserted_id}"
    response.content_type = "application/json"
    
    return response


@assistants_app.route("/assistants/list", methods=['GET'])
def get_assistants():
    return assistantService.list()


@assistants_app.route("/assistants/get/<id>", methods=['GET'])
def get_assistant(id):
    return assistantService.get(id)


@assistants_app.route("/assistants/update/<id>", methods=['PUT'])
def update_assistant(id):
    return assistantService.update(id, request)


@assistants_app.route("/assistants/delete/<id>", methods=['DELETE'])
def delete_assistant(id):
    return assistantService.delete(id)
