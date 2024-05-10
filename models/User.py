import os
from bson import ObjectId
import jwt

from utils.result import Result

class User:
  def __init__(self, id, email, password, name):
    self.id = id == None and ObjectId() or id;
    self.email = email
    self.password = password
    self.name = name
  
  def to_dict(self):
    return {
      "_id": self.id,
      "email": self.email,
      "password": self.password,
      "name": self.name
    }
  
  @staticmethod
  def decode_access_token(access_token):
    if isinstance(access_token, bytes):
        access_token = access_token.decode("utf-8")
    if access_token.startswith("Bearer "):
        split = access_token.split("Bearer")
        access_token = split[1].strip()
    try:
        key = os.getenv("SECRET")
        payload = jwt.decode(access_token, key, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        error = "Access token expired. Please log in again."
        return Result.Fail(error)
    except jwt.InvalidTokenError:
        error = "Invalid token. Please log in again."
        return Result.Fail(error)

    token_payload = dict(
        admin=payload["admin"],
        token=access_token,
        expires_at=payload["exp"],
    )
    return Result.Ok(token_payload)

def user_from_dict(dict):
  return User(dict["_id"], dict["email"], dict["password"], dict["name"])