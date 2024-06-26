from flask import request, jsonify
from flask import Blueprint

from services.DocumentService import DocumentService
from utils.tokendec import token_required

documents_app = Blueprint('documents_app', __name__)
documentService = DocumentService()


@documents_app.route("/documents/add", methods=['POST'])
@token_required
def add_document():
    inserted_id = documentService.insert_one(request)

    response_data = {"id": str(inserted_id)}
    response = jsonify(response_data)
    response.status_code = 201
    response.headers["Location"] = f"/documents/get/{inserted_id}"
    response.content_type = "application/json"

    return response


@documents_app.route("/documents/list", methods=['GET'])
@token_required
def list_documents():
    return documentService.list()


@documents_app.route("/documents/download/<id>", methods=['GET'])
@token_required
def get_document(id):
    return documentService.download(id)


@documents_app.route("/documents/path/get/<id>", methods=['GET'])
@token_required
def get_document_path(id):
    return documentService.get_path(id)


@documents_app.route("/documents/get/<id>", methods=['GET'])
@token_required
def get_document_info(id):
    return documentService.get(id)


@documents_app.route("/documents/delete/<id>", methods=['DELETE'])
def delete_document(id):
    return documentService.delete(id)
