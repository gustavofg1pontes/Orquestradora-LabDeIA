import requests

def createKnowledgeBase(assistantName):
    url = f'http://localhost:5000/api/v1/knowledge-base/{assistantName}'
    response = requests.post(url, '''docFilePath''')  # TODO get docFilePath by assistantName
    return response


def initSession(assistantName):
    url = f'http://localhost:5000/api/v1/llm/{assistantName}'
    response = requests.post(url, '''promptFilePath''')   #TODO get promptFilePath by assistantName
    return response

def sendCoreChat(assistantName, payload):
    url = f'http://localhost:5000/api/v1/llm/query/{assistantName}'
    response = requests.post(url, payload)
    return response


def closeSession(assistantName):
    url = f'http://localhost:5000/api/v1/llm/{assistantName}'
    response = requests.delete(url)
    return response

