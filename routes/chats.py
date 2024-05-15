from flask import request
from flask import Blueprint
from config.db import collection_config
from utils.tokendec import token_required
from services.ChatService import ChatService

chats_app = Blueprint('chats_app', __name__)
collection = collection_config("chats")
chatService = ChatService()


@chats_app.route('/chats/enviarMensagemLLM/<assistant_id>', methods=['POST'])
@token_required
def enviar_mensagem_llm(assistant_id):
    return chatService.insert_one(request, assistant_id)


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
