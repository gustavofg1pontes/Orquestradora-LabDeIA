import os

from bson import ObjectId
from flask import jsonify, send_from_directory
from werkzeug.utils import secure_filename

from models.Document import to_document, document_from_dict
from models.DocumentType import DocumentType
from repositories.DocumentRepository import DocumentRepository
from utils.documents import allowed_file


class DocumentService:
    def __init__(self):
        self.documentRepository = DocumentRepository()
        self.DOCUMENTS_FOLDER = 'documents'

    def insert_one(self, request):
        if 'file' not in request.files:
            return jsonify({"message": "Não há nenhum documento"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"message": "Não há nenhum documento"}), 400

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            document = to_document(self.DOCUMENTS_FOLDER, filename, request.form)
            assistant_folder = os.path.join(self.DOCUMENTS_FOLDER, document.assistant_id)
            document_folder = assistant_folder

            # Cria a pasta do assistente se ainda não existe
            os.makedirs(assistant_folder, exist_ok=True)

            if document.type == DocumentType.RAG:
                document_folder = os.path.join(assistant_folder, "knowledge")

            # Cria a pasta do documento se ainda não existe
            os.makedirs(document_folder, exist_ok=True)

            document.filepath = document_folder
            file.save(os.path.join(document_folder, filename))
            return self.documentRepository.insert(document.to_dict())

        return jsonify({"message": "Documento não inserido"}), 400

    def download(self, id):
        objId = ObjectId(id)
        document = document_from_dict(self.documentRepository.get(objId))
        if document:
            file_path = document.filepath
            file_name = document.filename
            if file_path and os.path.exists(os.path.join(file_path, file_name)):
                return send_from_directory(file_path, file_name, as_attachment=True)
            else:
                return jsonify({"error": "File not found or invalid file path"}), 404
        else:
            return jsonify({"error": "Documento não encontrado"}), 404

    def get(self, id):
        objId = ObjectId(id)
        document = self.documentRepository.get(objId)
        if document:
            document["_id"] = str(document["_id"])
            return jsonify(document), 200
        else:
            return jsonify({"error": "Documento não encontrado"}), 404

    def get_path(self, id):
        objId = ObjectId(id)
        document = document_from_dict(self.documentRepository.get(objId))
        filepath = os.path.join(document.filepath, document.filename)
        if document:
            return jsonify({"path": filepath}), 200
        else:
            return jsonify({"error": "Documento não encontrado"}), 404

    def list(self):
        documents = self.documentRepository.list()
        for document in documents:
            document["_id"] = str(document["_id"])
        return jsonify(documents), 200

    def delete(self, id):
        objId = ObjectId(id)
        document = document_from_dict(self.documentRepository.get(objId))
        os.remove(os.path.join(document.filepath, document.filename))
        return jsonify(self.documentRepository.delete(objId)), 200

    def update(self, id, model):
        obj_id = ObjectId(id)
        return jsonify(self.documentRepository.update(obj_id, model)), 200
