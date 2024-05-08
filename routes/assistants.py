from flask import request, jsonify
from flask import Blueprint
from config.db import collection_config

assistants_app = Blueprint('assistants_app', __name__)
collection = collection_config("assistants")


@assistants_app.route("/assistants/add", methods=['POST'])
def add_assistant():
    collection.insert_one(request.json)
    return jsonify({"message": f"Assistant inserido com sucesso"}), 200


@assistants_app.route("/assistants/list", methods=['GET'])
def get_assistants():
    assistants = list(collection.find())
    return jsonify(assistants), 200


@assistants_app.route("/assistants/update/<id>", methods=['PUT'])
def update_assistant(id):
    collection.update_one({"_id": id}, {"$set": request.json})
    return jsonify({"message": f"Assistente atualizada com sucesso"}), 200


@assistants_app.route("/assistants/delete/<id>", methods=['DELETE'])
def delete_assistante(id):
    collection.delete_one({"_id": id})
    return jsonify({"message": f"Assistente deletado com sucesso"}), 200
