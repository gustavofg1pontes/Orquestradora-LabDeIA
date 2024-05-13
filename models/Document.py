from datetime import datetime
from models.DocumentType import DocumentType

class Document:
    def __init__(self, filepath, filename, type, assistant_id, createdAt):
        self.filepath = filepath
        self.filename = filename
        self.type = type
        self.assistant_id = assistant_id
        self.createdAt = createdAt

    def to_dict(self):
        return {
            "filepath": self.filepath,
            "filename": self.filename,
            "type": self.type.name,
            "assistant_id": self.assistant_id,
            "createdAt": self.createdAt
        }


def document_from_dict(dict):
    return Document(dict["filepath"], dict["filename"], DocumentType(dict["type"].upper()), dict["assistant_id"], datetime.now())


def to_document(filepath, filename, dict):
    return Document(filepath, filename, DocumentType(dict["type"].upper()), dict["assistant_id"], datetime.now())
