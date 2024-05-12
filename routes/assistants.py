from bson import ObjectId
from flask import request, jsonify
from flask import Blueprint
from config.db import collection_config
from models.Assistant import to_assistant

assistants_app = Blueprint('assistants_app', __name__)
collection = collection_config("assistants")


@assistants_app.route("/assistants/add", methods=['POST'])
def add_assistant():
    assistant = to_assistant(request.json)

    inserted_id = collection.insert_one(assistant.to_dict()).inserted_id
    
    response_data = {"id": str(inserted_id)}
    response = jsonify(response_data)
    response.status_code = 201
    response.headers["Location"] = f"/assistants/get/{inserted_id}"
    response.content_type = "application/json"
    
    return response


@assistants_app.route("/assistants/list", methods=['GET'])
def get_assistants():
    assistants = list(collection.find())
    for assistant in assistants:
        assistant['_id'] = str(assistant['_id'])
    return jsonify(assistants), 200


@assistants_app.route("/assistants/get/<id>", methods=['GET'])
def get_assistant(id):
    objId = ObjectId(id)
    assistant = collection.find_one({"_id": objId})
    assistant['_id'] = str(assistant['_id'])
    return jsonify(assistant), 200


@assistants_app.route("/assistants/update/<id>", methods=['PUT'])
def update_assistant(id):
    objId = ObjectId(id)
    assitant = to_assistant(request.json)

    collection.update_one({"_id": objId}, {"$set": assitant.to_dict()})
    return jsonify({"message": f"Assistente atualizada com sucesso"}), 200


@assistants_app.route("/assistants/delete/<id>", methods=['DELETE'])
def delete_assistante(id):
    objId = ObjectId(id)
    collection.delete_one({"_id": objId})
    return jsonify({"message": f"Assistente deletado com sucesso"}), 200
