import os

from bson import ObjectId
from flask import request, jsonify, send_from_directory
from flask import Blueprint
from config.db import collection_config
from werkzeug.utils import secure_filename

from models.Document import to_document, document_from_dict
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
        inserted_id = collection.insert_one(document.to_dict()).inserted_id
        
        response_data = {"id": str(inserted_id)}
        response = jsonify(response_data)
        response.status_code = 201
        response.headers["Location"] = f"/documents/get/{inserted_id}"
        response.content_type = "application/json"
    
        return response
    return jsonify({"message": f"Documento não inserido"}), 400


@documents_app.route("/documents/list", methods=['GET'])
def list_documents():
    documents = list(collection.find())
    for document in documents:
        document['_id'] = str(document['_id'])
    return jsonify(documents), 200


@documents_app.route("/documents/get/<id>", methods=['GET'])
def get_document(id):
    objId = ObjectId(id)
    document = document_from_dict(collection.find_one({"_id": objId}))
    if document:
        file_path = document.filepath
        file_name = document.filename
        if file_path and os.path.exists(os.path.join(file_path, file_name)):
            return send_from_directory(file_path, file_name, as_attachment=True)
        else:
            return jsonify({"error": "File not found or invalid file path"}), 404
    else:
        return jsonify({"error": "Documento não encontrado"}), 404


@documents_app.route("/documents/delete/<id>", methods=['DELETE'])
def delete_document(id):
    objId = ObjectId(id)
    document = document_from_dict(collection.find_one({"_id": objId}))
    os.remove(os.path.join(DOCUMENTS_FOLDER, document.filename))
    collection.delete_one({"_id": objId})
    return jsonify({"message": f"Documento deletado com sucesso"}), 200
