from config.db import collection_config


class AuthRepository:
    def __init__(self):
        self.collection = collection_config("users")

    def insert(self, model):
        inserted = self.collection.insert_one(model)
        return inserted.inserted_id

    def delete(self, id):
        self.collection.delete_one({"_id": id})
        return {"message": "chat deletado com sucesso"}

    def get(self, id):
        return self.collection.find_one({"_id": id})

    def findByEmail(self, email):
        return self.collection.find_one({"email": email})

    def list(self):
        return list(self.collection.find())

    def update(self, model):
        self.collection.update_one({"_id": model.id}, {"$set": model})
        return {"message": "chat atualizado com sucesso"}

    def existsByEmail(self, email):
        return self.collection.count_documents({"email": email}) > 0
