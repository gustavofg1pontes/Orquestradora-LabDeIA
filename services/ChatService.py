from bson import ObjectId
from flask import jsonify

from models.Chat import to_chat
from repositories.ChatRepository import ChatRepository
from utils.core import send_core_chat


class ChatService:
    def __init__(self):
        self.chatRepository = ChatRepository()

    def insert_one(self, model, assistant_id):  # TODO: Terminar
        chat = to_chat(model)
        # history = self.chatRepository.get_history(chat.channel["id"])
        # payload = jsonify({"history": history, "query": chat.message})
        # response = send_core_chat(assistant_id, payload)

        # if response.status_code == 200:
        #    chat.response = response.json()
        #    self.chatRepository.insert(chat)
        # else:
        #    return jsonify({"error": "Assistente informado não existe"})
        #return chat.response

    def get(self, id):
        obj_id = ObjectId(id)
        chat = self.chatRepository.get(obj_id)
        chat["_id"] = str(chat["_id"])
        return jsonify(chat), 200

    def activate_chat(self, id):
        chat = self.chatRepository.get_by_channel_id(id)
        if chat:
            self.chatRepository.update({"_id": chat["_id"], "active": True})
            return jsonify({"message": f"Chat com ID {id} atualizado com sucesso"}), 200
        else:
            return jsonify({"error": "Chat não encontrado"}), 404

    def inactivate_chat(self, id):
        chat = self.chatRepository.get_by_channel_id(id)
        if chat:
            self.chatRepository.update({"_id": chat["_id"], "active": False})
            return jsonify({"message": f"Chat com ID {id} atualizado com sucesso"}), 200
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
        return jsonify(chats)
