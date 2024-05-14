from datetime import datetime

class Assistant:
    def __init__(self, name, owner_id, createdAt):
        self.name = name
        #self.owner_id = owner_id
        self.createdAt = createdAt

    def to_dict(self):
        return {
            "name": self.name,
            #"owner_id": self.owner_id,
            "createdAt": self.createdAt
        }


def to_assistant(dict):
    return Assistant(dict["name"], dict["owner_id"], datetime.now())
