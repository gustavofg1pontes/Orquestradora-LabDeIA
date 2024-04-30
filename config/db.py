import os
from dotenv import load_dotenv

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()


def db_config():
    # Configurando bdd
    uri = os.getenv("DB_URL")
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client["LabDeIA"]
    collection = db["chats"]
    return collection
