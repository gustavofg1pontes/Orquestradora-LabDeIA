from config.db import collection_config


class DocumentRepository:
    def __init__(self):
        self.collection = collection_config("documents")

    def insert(self, model):
        inserted_id = self.collection.insert_one(model).inserted_id
        return inserted_id

    def delete(self, id):
        self.collection.delete_one({"_id": id})
        return {"message": "Document deleted"}

    def get(self, id):
        return self.collection.find_one({"_id": id})

    def list(self):
        return list(self.collection.find())

    def update(self, id, model):
        self.collection.update_one({"_id": id}, {"$set": model})
