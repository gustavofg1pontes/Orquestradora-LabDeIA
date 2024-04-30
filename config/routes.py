from flask import request, jsonify
from config.app import app_config
from config.db import db_config

app = app_config()
collection = db_config()


@app.route('/enviarMensagemLLM', methods=['POST'])
def enviar_mensagem_llm():
    chat = collection.find_one({"id": request.json['id']})
    if not chat:
        resultado = collection.insert_one(request.json)
        chat = collection.find_one({"_id": resultado.inserted_id})

    chat["message"] = request.json['message']
    # TODO enviar p llm
    newvalues = {"$set": {"message": chat["message"], "step": 2}}  # +} TODO concatenate llm response and change step value
    filter = {"_id": chat["_id"]}
    collection.update_one(filter, newvalues)
    return jsonify({"message": f"LLM Message"}), 200


@app.route("/desativar/<id>", methods=['PUT'])
def desativar(id):
    chat = collection.find_one({"id": id})
    if chat:
        collection.update_one({"id": id}, {"$set": {"active": False}})
        return jsonify({"message": f"Chat com ID {id} atualizado com sucesso"}), 200
    else:
        return jsonify({"error": "Chat não encontrado"}), 404


@app.route("/ativar/<id>", methods=['PUT'])
def ativar(id):
    chat = collection.find_one({"id": id})
    if chat:
        collection.update_one({"id": id}, {"$set": {"active": True}})
        return jsonify({"message": f"Chat com ID {id} atualizado com sucesso"}), 200
    else:
        return jsonify({"error": "Chat não encontrado"}), 404


@app.route("/chat/<id>", methods=['GET'])
def get(id):
    chat = collection.find_one({"_id": id})
    if chat:
        return jsonify(chat), 200
    else:
        return jsonify({"error": "Chat não encontrado"}), 404


@app.route("/listar", methods=['GET'])
def listar():
    chats = list(collection.find())
    return jsonify(chats), 200


@app.route("/listarAtivos", methods=['GET'])
def listar_ativos():
    chats_ativos = list(collection.find({"active": True}))
    return jsonify(chats_ativos), 200


@app.route("/listarInativos", methods=['GET'])
def listar_inativos():
    chats_inativos = list(collection.find({"active": False}))
    return jsonify(chats_inativos), 200
