from repositories.DocumentRepository import DocumentRepository


class DocumentService:
    def __init__(self):
        self.documentRepository = DocumentRepository()

    def insert_one(self, model):
        self.documentRepository.insert(model)

    def get(self, id):
        return self.documentRepository.get(id)

    def list(self):
        return self.documentRepository.list()

    def delete(self, id):
        self.documentRepository.delete(id)

    def update(self, id, model):
        self.documentRepository.update(id, model)
