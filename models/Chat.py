class Chat:
    def __init__(self, id, username, step, active):
        self.id = id
        self.username = username
        self.step = step
        self.active = active
        self.messages = []

    def add_message(self, message):
        self.messages.append(message)

    def get_messages(self):
        return self.messages

    def get_last_message(self):
        return self.messages[-1]