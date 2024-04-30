from flask import Flask, request, jsonify
import os
import bson
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()

# Configurando bdd
uri = os.getenv("DB_URL")
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["LabDeIA"]
collection = db["chats"]

app = Flask(__name__)


@app.route('/enviarMensagemLLM', methods=['POST'])
def enviarMensagemLLM():
    chat = collection.find_one({"id": request.json['id']})
    if not chat:
        resultado = collection.insert_one(request.json)
        chat = collection.find_one({"_id": resultado.inserted_id})

    chat["message"] = request.json['message']
    # TODO enviar p llm
    newvalues = {"$set": {"message": chat, "step": 2}}  # +} TODO concatenate llm response and change step value
    filter = {"_id": chat["_id"]}
    collection.update_one(filter, newvalues)
    return jsonify({"message": f"LLM Message"}), 200


@app.route("/desativar/<id>", methods=['PUT'])
def desativar(id):
    chat = collection.find_one({"id": id})
    if chat:
        collection.update_one({"id": id}, {"$set": {"active": False}})
        return jsonify({"message": f"Chat com ID {id} atualizado com sucesso"}), 200
    else:
        return jsonify({"error": "Chat não encontrado"}), 404


@app.route("/ativar/<id>", methods=['PUT'])
def ativar(id):
    chat = collection.find_one({"id": id})
    if chat:
        collection.update_one({"id": id}, {"$set": {"active": True}})
        return jsonify({"message": f"Chat com ID {id} atualizado com sucesso"}), 200
    else:
        return jsonify({"error": "Chat não encontrado"}), 404


@app.route("/chat/<id>", methods=['GET'])
def get(id):
    chat = collection.find_one({"_id": id})
    if chat:
        return jsonify(chat), 200
    else:
        return jsonify({"error": "Chat não encontrado"}), 404


@app.route("/listar", methods=['GET'])
def listar():
    chats = list(collection.find())
    return jsonify(chats), 200


@app.route("/listarAtivos", methods=['GET'])
def listarAtivos():
    chats_ativos = list(collection.find({"active": True}))
    return jsonify(chats_ativos), 200


@app.route("/listarInativos", methods=['GET'])
def listarInativos():
    chats_inativos = list(collection.find({"active": False}))
    return jsonify(chats_inativos), 200


if __name__ == '__main__':
    app.run()
