from repositories.documentRepository import DocumentRepository


class DocumentService:
    def __init__(self):
        self.documentRepository = DocumentRepository()
