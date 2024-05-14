from enum import Enum


class DocumentType(str, Enum):
    PROMPT = "PROMPT"
    RAG = "RAG"
