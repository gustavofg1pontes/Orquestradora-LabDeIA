class Chat:
    def __init__(self, id, message_service, username, step, active, message, response, createdAt):
        self.channel = {
            id, message_service
        }
        self.username = username
        self.step = step
        self.isActive = active
        self.message = message
        self.response = response
        self.createdAt = createdAt

    def to_dict(self):
        return {
            "id": self.channel["id"],
            "message_service": self.channel["message_service"],
            "username": self.username,
            "step": self.step,
            "active": self.isActive,
            "message": self.message,
            "response": self.response,
            "createdAt": self.createdAt
        }

    def desativar(self):
        self.isActive = False

    def ativar(self):
        self.isActive = True

    @staticmethod
    def to_chat(dict):
        return Chat(dict["id"], dict["message_service"], dict["username"], dict["step"], dict["active"],
                    dict["message"], dict["response"], dict["createdAt"])
