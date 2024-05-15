from config.db import collection_config


class ChatRepository:
    def __init__(self):
        self.collection = collection_config("chats")

    def insert(self, model):
        inserted = self.collection.insert_one(model)
        return inserted.inserted_id

    def update(self, id, model):
        self.collection.update_many({"channel.id": id}, {"$set": model})
        return {"message": "chat atualizado com sucesso"}

    def delete(self, id):
        self.collection.delete_one({"_id": id})
        return {"message": "chat deletado com sucesso"}

    def get(self, channel_id):
        assistant = list(self.collection.find({"channel.id": channel_id}))
        return assistant

    def get_history(self, id):
        history = list(self.collection
                       .find({"channel.id": id}, {"message": 1, "response": 1, "_id": 0})
                       .sort("createdAt", -1).limit(20))[::-1]
        return history

    def get_by_channel_id(self, id):
        chat = self.collection.find_one({"channel.id": id})
        return chat

    def list(self):
        return list(self.collection.find())

    def list_actives(self):
        return list(self.collection.find({"active": True}))

    def list_inactives(self):
        return list(self.collection.find({"active": False}))
