from flask import request, jsonify
from flask import Blueprint
from config.db import collection_config
from models import Chat
from models.Chat import to_chat

chats_app = Blueprint('chats_app', __name__)
collection = collection_config("chats")


@chats_app.route('/chats/enviarMensagemLLM', methods=['POST'])
def enviar_mensagem_llm():
    chat = to_chat(request.json)

    history = collection.find().sort({"createdAt": -1}).limit(5)

    # TODO request llm response using history and chat.message
    chat.response = "resposta"

    collection.insert_one(chat.to_dict())
    return jsonify({"message": chat.response}), 200  # TODO retornar a resposta da LLM"""


@chats_app.route("/chats/desativar/<id>", methods=['PUT'])
def desativar(id):
    chat = collection.find_one({"id": id})
    if chat:
        collection.update_one({"id": id}, {"$set": {"active": False}})
        return jsonify({"message": f"Chat com ID {id} atualizado com sucesso"}), 200
    else:
        return jsonify({"error": "Chat não encontrado"}), 404


@chats_app.route("/chats/ativar/<id>", methods=['PUT'])
def ativar(id):
    chat = collection.find_one({"id": id})
    if chat:
        collection.update_one({"id": id}, {"$set": {"active": True}})
        return jsonify({"message": f"Chat com ID {id} atualizado com sucesso"}), 200
    else:
        return jsonify({"error": "Chat não encontrado"}), 404


@chats_app.route("/chats/get/<id>", methods=['GET'])
def get(id):
    chat = collection.find_one({"_id": id})
    if chat:
        return jsonify(chat), 200
    else:
        return jsonify({"error": "Chat não encontrado"}), 404


@chats_app.route("/chats/list", methods=['GET'])
def listar():
    chats = list(collection.find())
    return jsonify(chats), 200


@chats_app.route("/chats/listarAtivos", methods=['GET'])
def listar_ativos():
    chats_ativos = list(collection.find({"active": True}))
    return jsonify(chats_ativos), 200


@chats_app.route("/chats/listarInativos", methods=['GET'])
def listar_inativos():
    chats_inativos = list(collection.find({"active": False}))
    return jsonify(chats_inativos), 200
