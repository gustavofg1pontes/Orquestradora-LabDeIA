from flask import request, jsonify
from flask import Blueprint

from config.assistant import AssistantConfig
from services.AssistantService import AssistantService
from utils.apiKey import api_key_required
from utils.tokendec import token_required
from services.ChatService import ChatService

chats_app = Blueprint('chats_app', __name__)
chatService = ChatService()
assistantService = AssistantService()


@chats_app.route('/chats/enviarMensagemLLM', methods=['POST'])
@api_key_required
def enviar_mensagem_llm():
    # Get the assistant_id from the X-API-Key header
    api_key_header = request.headers.get('X-API-Key')

    assistant_id = assistantService.findByKey(api_key_header)["_id"]
    if not assistant_id:
        return jsonify({"message": "Invalid X-API-Key"}), 401

    AssistantConfig.set_assistant_id(assistant_id)
    return chatService.insert_one(request.json)


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
