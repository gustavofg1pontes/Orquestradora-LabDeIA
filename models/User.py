class User:
  def __init__(self, id, email, password, name):
    self.id = id;
    self.email = email
    self.password = password
    self.name = name
  
  def to_dict(self):
    return {
      "id": self.id,
      "email": self.email,
      "password": self.password,
      "name": self.name
    }

def user_from_dict(dict):
  return User(dict["id"], dict["email"], dict["password"], dict["name"])