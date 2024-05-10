from bson import ObjectId
from flask import request, jsonify
from flask import Blueprint
from config.db import collection_config
from models.Chat import to_chat
from utils.tokendec import token_required

chats_app = Blueprint('chats_app', __name__)
collection = collection_config("chats")


@chats_app.route('/chats/enviarMensagemLLM', methods=['POST'])
@token_required
def enviar_mensagem_llm():
    chat = to_chat(request.json)

    history = collection.find({"id": chat.channel["id"]}).sort({"createdAt": -1}).limit(5)

    # TODO request llm response using history and chat.message
    chat.response = "resposta"

    collection.insert_one(chat.to_dict())
    return jsonify({"message": chat.response}), 200  # TODO retornar a resposta da LLM"""


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
    chat["_id"] = str(chat["_id"])
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
