from bson import ObjectId
from flask import request, jsonify
from flask import Blueprint
from config.db import collection_config
from models.Chat import to_chat
from utils.apiKey import api_key_required
from utils.tokendec import token_required
from utils.core import send_core_chat
from services.ChatService import ChatService

chats_app = Blueprint('chats_app', __name__)
collection = collection_config("chats")
chatService = ChatService()

@chats_app.route('/chats/enviarMensagemLLM', methods=['POST'])
@api_key_required
def enviar_mensagem_llm(assistant_id):  #TODO: verify if the chat is active = True, else return error: chat inactive
    chat = to_chat(request.json)

    history = list(collection.find({"channel.id": chat.channel['id']}, {"message": 1, "response": 1, "_id": 0}).sort("createdAt", -1).limit(20))[::-1]
    payload = jsonify({"history": history, "query": chat.message})
    response = send_core_chat(assistant_id, payload)

    if response.status_code == 200:
        chat.response = response.json()
    else:
        return jsonify({"error": "Assistente informado não existe"}), 404

    collection.insert_one(chat.to_dict())
    return jsonify({"response": chat.response}), 200


@chats_app.route("/chats/ativar/<channel_id>", methods=['PUT'])
@token_required
def ativar(channel_id):
    return chatService.activate_chat(channel_id)


@chats_app.route("/chats/desativar/<channel_id>", methods=['PUT'])
@token_required
def desativar(channel_id):
    return chatService.inactivate_chat(channel_id)


@chats_app.route("/chats/get/<channel_id>", methods=['GET'])
@token_required
def get(channel_id):
    return chatService.get(channel_id)


@chats_app.route("/chats/list", methods=['GET'])
@token_required
def listar():
    return chatService.list()


@chats_app.route("/chats/listarAtivos", methods=['GET'])
@token_required
def listar_ativos():
    return chatService.list_actives()


@chats_app.route("/chats/listarInativos", methods=['GET'])
@token_required
def listar_inativos():
    return chatService.list_inactives()
