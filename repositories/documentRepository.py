from config.db import collection_config


class DocumentRepository:
    def __init__(self):
        self.collection = collection_config("documents")
    def insert(self, model):
        self.collection.insert_one(model)

    def delete(self, id):
        self.collection.delete_one({"_id": id})

    def get(self, id):
        self.collection.find_one({"_id": id})

    def list(self):
        return list(self.collection.find())

    def update(self, model):
        self.collection.update_one({"_id": model.id}, {"$set": model})
