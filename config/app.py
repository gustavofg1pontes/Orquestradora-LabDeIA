from flask import Flask
from .db import db_config


def app_config():
    app = Flask(__name__)
    return app
