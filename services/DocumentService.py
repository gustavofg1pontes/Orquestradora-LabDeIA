from repositories.DocumentRepository import DocumentRepository


class DocumentService:
    def __init__(self):
        self.documentRepository = DocumentRepository()
