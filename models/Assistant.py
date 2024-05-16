from datetime import datetime

from utils.apiKey import generate_key


class Assistant:
    def __init__(self, name, owner_id, createdAt):
        self.name = name
        self.owner_id = owner_id
        self.api_key = generate_key()
        self.createdAt = createdAt

    def to_dict(self):
        return {
            "name": self.name,
            "owner_id": self.owner_id,
            "api_key": self.api_key,
            "createdAt": self.createdAt
        }


def to_assistant(dict):
    return Assistant(dict["name"], dict["owner_id"], datetime.now())
