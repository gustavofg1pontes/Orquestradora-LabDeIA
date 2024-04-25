from flask import Flask
from flask import request
import os
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()
uri = os.getenv("DB_URL")

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

app = Flask(__name__)


@app.route('/enviarMensagemLLM', methods=['POST'])
def enviarMensagemLLM():
    request.data  # id, username e a message
    # enviar pra llm -> step e a msg resposta
    # Editar no mongo o usuario do id
    # retorna msg resposta


@app.route("/desativar/<id>", methods=['POST'])
def desativar(id):
    print()  # Editar no mongo o usuario do id
    # retorna msg resposta


@app.route("/ativar/<id>", methods=['POST'])
def ativar(id):
    print()  # Editar no mongo o usuario do id


@app.route("/chat/<id>", methods=['GET'])
def get(id):
    print()  # retorna o chat do id


@app.route("/listar", methods=['GET'])
def listar():
    print()  # lista todos chats


@app.route("/listarAtivos", methods=['GET'])
def listarAtivos():
    print()  # lista todos chats ativos


@app.route("/listarInativos", methods=['GET'])
def listarInativos():
    print()  # lista todos chats inativos


if __name__ == '__main__':
    app.run()

'''
uri = "mongodb+srv://gpontesf06:8gd8IDUg2HfFYxTs@labdeia.ibq65h9.mongodb.net/?retryWrites=true&w=majority&appName=labdeia"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Selecionando o banco de dados
db = client["LabDeIA"]

# Selecionando a coleção
collection = db["chats"]
documentos = collection.find({"chave3" : "valor3"})
for documento in documentos:
    print(documento)

# Dados a serem inseridos
dados = {"chave1": "valor1", "chave2": "valor2"}

# Inserindo os dados na coleção
resultado = collection.insert_one(dados)

# Imprimindo o ID do documento inserido
print("ID do documento inserido:", resultado.inserted_id)
'''
