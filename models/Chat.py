class Chat:
    def __init__(self, id, username, step, active, message):
        self.id = id
        self.username = username
        self.step = step
        self.active = active
        self.message = message

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "step": self.step,
            "active": self.active,
            "message": self.message
        }

    def desativar(self):
        self.active = False

    def ativar(self):
        self.active = True
