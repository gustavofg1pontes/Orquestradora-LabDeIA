from flask import jsonify

from models.Chat import to_chat
from repositories.ChatRepository import ChatRepository
from utils.core import send_core_chat


class ChatService:
    def __init__(self):
        self.chatRepository = ChatRepository()

    def insert_one(self, model):
        chat = to_chat(model)
        if not chat.isActive:
            return jsonify({"error": "Chat inativo"}), 404

        history = self.chatRepository.get_history(chat.channel["id"])
        payload = {"history": history, "query": chat.message}

        response = send_core_chat(chat.assistant_id, payload)

        if response.status_code != 200:
            return jsonify({"error": "Assistente informado não existe"}), 404

        response_json = response.json()
        if "response" not in response_json:
            return jsonify({"error": "Não foi encontrado uma resposta do core"}), 404

        chat.response = response_json["response"]
        chat.tokens["in"] = response_json["tokens"]["in"]
        chat.tokens["out"] = response_json["tokens"]["out"]

        self.chatRepository.insert(chat.to_dict())
        return jsonify({"response": chat.response}), 200

    def get(self, channel_id):
        chats = self.chatRepository.get(channel_id)
        for chat in chats:
            chat["_id"] = str(chat["_id"])
        if chats:
            return jsonify(chats), 200
        else:
            return jsonify({"error": "Chat não encontrado"}), 404

    def activate_chat(self, channel_id):
        chat = self.chatRepository.get_by_channel_id(channel_id)
        if chat:
            self.chatRepository.update(channel_id, {"active": True})
            return jsonify({"message": f"Chat com ID {channel_id} atualizado com sucesso"}), 200
        else:
            return jsonify({"error": "Chat não encontrado"}), 404

    def inactivate_chat(self, channel_id):
        chat = self.chatRepository.get_by_channel_id(channel_id)
        if chat:
            self.chatRepository.update(channel_id, {"active": False})
            return jsonify({"message": f"Chat com ID {channel_id} atualizado com sucesso"}), 200
        else:
            return jsonify({"error": "Chat não encontrado"}), 404

    def list(self):
        chats = self.chatRepository.list()
        for chat in chats:
            chat["_id"] = str(chat["_id"])
        return jsonify(chats), 200

    def list_actives(self):
        chats = self.chatRepository.list_actives()
        for chat in chats:
            chat["_id"] = str(chat["_id"])
        return jsonify(chats), 200

    def list_inactives(self):
        chats = self.chatRepository.list_inactives()
        for chat in chats:
            chat["_id"] = str(chat["_id"])
        return jsonify(chats), 200
