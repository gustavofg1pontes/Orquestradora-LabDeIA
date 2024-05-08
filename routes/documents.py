import os
from flask import request, jsonify
from flask import Blueprint
from config.db import collection_config
from werkzeug.utils import secure_filename

documents_app = Blueprint('documents_app', __name__)
collection = collection_config("documents")
documents_app.config['UPLOAD_FOLDER'] = './documents'


@documents_app.route("/documents/add", methods=['POST'])
def add_document():
    if 'file' not in request.files:
        return jsonify({"message": f"Não há nenhum documento"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": f"Não há nenhum documento"}), 400
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(documents_app.config['UPLOAD_FOLDER'], filename))

        collection.insert_one({"filepath": f"./documents/{filename}", "type": request.form["type"]})

        return jsonify({"message": f"Documento inserido com sucesso"}), 200
    return jsonify({"message": f"Documento não inserido"}), 400


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
