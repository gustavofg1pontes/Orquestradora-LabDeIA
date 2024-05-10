class Assistant:
    def __init__(self, name, company, createdAt):
        self.name = name
        self.company = company
        self.createdAt = createdAt

    def to_dict(self):
        return {
            "name": self.name,
            "company": self.company,
            "createdAt": self.createdAt
        }


def to_assistant(dict):
    return Assistant(dict["name"], dict["company"], dict["createdAt"])
