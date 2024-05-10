from flask import Flask

from routes.documents import documents_app
from routes.chats import chats_app
from routes.assistants import assistants_app
from routes.auth import auth_api

app = Flask(__name__)

app.register_blueprint(assistants_app)
app.register_blueprint(documents_app)
app.register_blueprint(chats_app)
app.register_blueprint(auth_api)

if __name__ == '__main__':
    app.run()
