import os

from bson import ObjectId
from flask import request, jsonify, send_from_directory
from flask import Blueprint

import main
from config.db import collection_config
from werkzeug.utils import secure_filename

from models.DocumentType import DocumentType
from models.Document import to_document, document_from_dict
from utils.documents import allowed_file

DOCUMENTS_FOLDER = 'documents'

documents_app = Blueprint('documents_app', __name__)
collection = collection_config("documents")
collection_assistans = collection_config("assistants")

@documents_app.route("/documents/add", methods=['POST'])
def add_document():
    if 'file' not in request.files:
        return jsonify({"message": f"Não há nenhum documento"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": f"Não há nenhum documento"}), 400
    if not request.form['assistant_id'] == collection_assistans.find_one({"_id": ObjectId(request.form['assistant_id'])}):
        return jsonify({"message": f"Não há nenhum assistente com esse id"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

        document = to_document(DOCUMENTS_FOLDER, filename, request.form)
        assistant_folder = os.path.join(DOCUMENTS_FOLDER, document.assistant_id)
        document_folder = assistant_folder
        if not os.path.exists(assistant_folder):
            os.makedirs(assistant_folder)

        if document.type == DocumentType.RAG:
            rag_folder = os.path.join(assistant_folder, "knowledge")
            if not os.path.exists(rag_folder):
                os.makedirs(rag_folder)
            document_folder = rag_folder

        file.save(os.path.join(document_folder, filename))


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


@documents_app.route("/documents/download/<id>", methods=['GET'])
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


@documents_app.route("/documents/path/get/<id>", methods=['GET'])
def get_document_path(id):
    objId = ObjectId(id)
    document = document_from_dict(collection.find_one({"_id": objId}))
    filepath = os.path.join(main.app.root_path, document.filepath, document.filename).replace("\\", "/")
    if document:
        return jsonify({"path": filepath}), 200
    else:
        return jsonify({"error": "Documento não encontrado"}), 404


@documents_app.route("/documents/get/<id>", methods=['GET'])
def get_document_info(id):
    objId = ObjectId(id)
    document = collection.find_one({"_id": objId})
    document["_id"] = str(document["_id"])
    if document:
        return jsonify(document), 200
    else:
        return jsonify({"error": "Documento não encontrado"}), 404


@documents_app.route("/documents/delete/<id>", methods=['DELETE'])
def delete_document(id):
    objId = ObjectId(id)
    document = document_from_dict(collection.find_one({"_id": objId}))
    os.remove(os.path.join(DOCUMENTS_FOLDER, document.filename))
    collection.delete_one({"_id": objId})
    return jsonify({"message": f"Documento deletado com sucesso"}), 200
