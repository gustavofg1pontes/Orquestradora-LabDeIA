from datetime import datetime

from config.assistant import AssistantConfig


class Chat:
    def __init__(self, id, message_service, username, active, message, createdAt):
        self.channel = {
            "id": id,
            "message_service": message_service
        }
        self.tokens = {
            "in": "",
            "out": ""
        }
        self.username = username
        self.assistant_id = AssistantConfig.get_assistant_id()
        self.isActive = active
        self.message = message
        self.response = ""
        self.tokensCount = {
            "in": 0,
            "out": 0
        }
        self.createdAt = createdAt

    def to_dict(self):
        return {
            "channel": {
                "id": self.channel["id"],
                "message_service": self.channel["message_service"]
            },
            "tokens": {
                "in": self.tokens["in"],
                "out": self.tokens["out"]
            },
            "username": self.username,
            "assistant_id": self.assistant_id,
            "active": self.isActive,
            "message": self.message,
            "response": self.response,
            "tokensCount": {
                "in": self.tokensCount["in"],
                "out": self.tokensCount["out"]
            },
            "createdAt": self.createdAt
        }

    def desativar(self):
        self.isActive = False

    def ativar(self):
        self.isActive = True


def to_chat(dict):
    return Chat(dict["id"], dict["message_service"], dict["username"], dict["active"],
                dict["message"], datetime.now())
