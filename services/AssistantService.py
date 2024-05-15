from bson import ObjectId
from flask import jsonify

from models.Assistant import to_assistant
from repositories.AssistantRepository import AssistantRepository
from utils.apiKey import generate_and_save_key


class AssistantService:
    def __init__(self):
        self.assistantRepository = AssistantRepository()

    def insert_one(self, model):
        assistant = to_assistant(model)
        if not assistant.name:
            return jsonify({"message": "Assistant name can't be null"}), 400
        if not assistant.owner_id:
            return jsonify({"message": "Owner id can't be null"}), 400
        inserted_id = self.assistantRepository.insert(assistant.to_dict())
        token = generate_and_save_key(inserted_id)

        return {
            "id": str(inserted_id),
            "token": token
        }

    def get(self, id):
        obj_id = ObjectId(id)
        assistant = self.assistantRepository.get(obj_id)
        assistant["_id"] = str(assistant["_id"])
        return jsonify(assistant), 200

    def list(self):
        assistants = self.assistantRepository.list()
        for assistant in assistants:
            assistant["_id"] = str(assistant["_id"])
        return jsonify(assistants), 200

    def delete(self, id):
        obj_id = ObjectId(id)
        return jsonify(self.assistantRepository.delete(obj_id)), 200

    def update(self, id, model):
        obj_id = ObjectId(id)
        return jsonify(self.assistantRepository.update(obj_id, model)), 200
