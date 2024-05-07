from flask import request, jsonify
from flask import Blueprint
from config.db import db_config

documents_app = Blueprint('documents_app', __name__)
collection = db_config("documents")


@documents_app.route("/documents/add", methods=['POST'])
def add_document():
    collection.insert_one(request.json)
    return jsonify({"message": f"Documento inserido com sucesso"}), 200


@documents_app.route("/documents/list", methods=['GET'])
def get_documents():
    documents = list(collection.find())
    return jsonify(documents), 200


@documents_app.route("/documents/update/<id>", methods=['PUT'])
def update_document(id):
    collection.update_one({"_id": id}, {"$set": request.json})
    return jsonify({"message": f"Documento atualizado com sucesso"}), 200


@documents_app.route("/documents/delete/<id>", methods=['DELETE'])
def delete_document(id):
    collection.delete_one({"_id": id})
    return jsonify({"message": f"Documento deletado com sucesso"}), 200

