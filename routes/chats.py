from bson import ObjectId
from flask import request, jsonify
from flask import Blueprint
from config.db import collection_config
from models.Chat import to_chat
from utils.tokendec import token_required
from utils.coreRoutes import initSession, sendCoreChat, closeSession

chats_app = Blueprint('chats_app', __name__)
collection = collection_config("chats")


@chats_app.route('/chats/enviarMensagemLLM/<assistantName>', methods=['POST'])
@token_required
def enviar_mensagem_llm(assistantName):
    chat = to_chat(request.json)
    initSession(assistantName) # TODO see utils/coreRoutes.py

    history = list(collection.find({"channel.id": chat.channel['id']}, {"message": 1, "response": 1, "_id": 0}).sort("createdAt", -1).limit(20))[::-1]
    payload = jsonify({"history": history, "query": chat.message})
    response = sendCoreChat(assistantName, payload)

    if response.status_code == 200:
        chat.response = response.json()
    else:
        return jsonify({"error": "Assistente informado não existe"}), 404

    collection.insert_one(chat.to_dict())
    closeSession(assistantName)
    return jsonify({"response": chat.response}), 200


@chats_app.route("/chats/desativar/<id>", methods=['PUT'])
@token_required
def desativar(id):
    chat = collection.find_one({"channel.id": id})
    if chat:
        collection.update_one({"channel.id": id}, {"$set": {"active": False}})
        return jsonify({"message": f"Chat com ID {id} atualizado com sucesso"}), 200
    else:
        return jsonify({"error": "Chat não encontrado"}), 404


@chats_app.route("/chats/ativar/<id>", methods=['PUT'])
@token_required
def ativar(id):
    chat = collection.find_one({"channel.id": id})
    if chat:
        collection.update_one({"channel.id": id}, {"$set": {"active": True}})
        return jsonify({"message": f"Chat com ID {id} atualizado com sucesso"}), 200
    else:
        return jsonify({"error": "Chat não encontrado"}), 404


@chats_app.route("/chats/get/<id>", methods=['GET'])
@token_required
def get(id):
    objId = ObjectId(id)
    chat = collection.find_one({"_id": objId})
    chat['_id'] = str(chat['_id'])
    if chat:
        return jsonify(chat), 200
    else:
        return jsonify({"error": "Chat não encontrado"}), 404


@chats_app.route("/chats/list", methods=['GET'])
@token_required
def listar():
    chats = list(collection.find())
    for chat in chats:
        chat['_id'] = str(chat['_id'])
    return jsonify(chats), 200


@chats_app.route("/chats/listarAtivos", methods=['GET'])
@token_required
def listar_ativos():
    chats_ativos = list(collection.find({"active": True}))
    for chat in chats_ativos:
        chat['_id'] = str(chat['_id'])
    return jsonify(chats_ativos), 200


@chats_app.route("/chats/listarInativos", methods=['GET'])
@token_required
def listar_inativos():
    chats_inativos = list(collection.find({"active": False}))
    for chat in chats_inativos:
        chat['_id'] = str(chat['_id'])
    return jsonify(chats_inativos), 200
