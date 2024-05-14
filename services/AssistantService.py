from bson import ObjectId
from models.Assistant import to_assistant
from repositories.AssistantRepository import AssistantRepository


class AssistantService:
    def __init__(self):
        self.assistantRepository = AssistantRepository()

    def insert_one(self, model):
        assistant = to_assistant(model)
        if not assistant.name:
            return {"message": "Assistant name can't be null"}
        #if not assistant.owner_id:
        #    return {"message": "Assistant owner_id can't be null"}

        return self.assistantRepository.insert(assistant)

    def get(self, id):
        obj_id = ObjectId(id)
        assistant = self.assistantRepository.get(obj_id)
        assistant["_id"] = str(assistant["_id"])
        return assistant

    def list(self):
        assistants = self.assistantRepository.list()
        for assistant in assistants:
            assistant["_id"] = str(assistant["_id"])
        return assistants

    def delete(self, id):
        obj_id = ObjectId(id)
        return self.assistantRepository.delete(obj_id)

    def update(self, id, model):
        return self.assistantRepository.update(id, model)
