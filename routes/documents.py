import os

from bson import ObjectId
from flask import request, jsonify, send_from_directory
from flask import Blueprint
from config.db import collection_config
from werkzeug.utils import secure_filename

from models.Document import to_document
from utils.documents import allowed_file

DOCUMENTS_FOLDER = '.\\documents'

documents_app = Blueprint('documents_app', __name__)
collection = collection_config("documents")


@documents_app.route("/documents/add", methods=['POST'])
def add_document():
    if 'file' not in request.files:
        return jsonify({"message": f"Não há nenhum documento"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": f"Não há nenhum documento"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(DOCUMENTS_FOLDER, filename))

        document = to_document(DOCUMENTS_FOLDER, filename, request.form)
        collection.insert_one(document.to_dict())
        return jsonify({"message": f"Documento inserido com sucesso"}), 200
    return jsonify({"message": f"Documento não inserido"}), 400


@documents_app.route("/documents/list", methods=['GET'])
def list_documents():
    documents = list(collection.find())
    for document in documents:
        document['_id'] = str(document['_id'])
    return jsonify(documents), 200


@documents_app.route("/documents/get/<string:id>", methods=['GET'])
def get_document(id):
    objId = ObjectId(id)
    document = collection.find_one({"_id": objId})
    if document:
        file_path = document.get("filepath")
        file_name = document.get("filename")
        if file_path and os.path.exists(file_path + f"\\{file_name}"):
            return send_from_directory(file_path, file_name, as_attachment=True)
        else:
            return jsonify({"error": "File not found or invalid file path"}), 404
    else:
        return jsonify({"error": "Documento não encontrado"}), 404


'''
@documents_app.route("/documents/list", methods=['GET'])
def list_documents():
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
'''
