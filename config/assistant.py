class AssistantConfig:
    _assistant_id = ''

    @staticmethod
    def set_assistant_id(id):
        AssistantConfig._assistant_id = id

    @staticmethod
    def get_assistant_id():
        return AssistantConfig._assistant_id
