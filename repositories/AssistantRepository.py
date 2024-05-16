from config.db import collection_config


class AssistantRepository:
    def __init__(self):
        self.collection = collection_config("assistants")

    def insert(self, model):
        inserted_id = self.collection.insert_one(model).inserted_id
        return inserted_id

    def delete(self, id):
        self.collection.delete_one({"_id": id})
        return {"message": "Assistente deletado com sucesso"}

    def get(self, id):
        assistant = self.collection.find_one({"_id": id})
        return assistant

    def findByKey(self, key):
        assistant = self.collection.find_one({"api_key": key})
        return assistant

    def list(self):
        return list(self.collection.find())

    def update(self, id, model):
        self.collection.update_one({"_id": id}, {"$set": model})
        return {"message": "Assistente atualizado com sucesso"}
