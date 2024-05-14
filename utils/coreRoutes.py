import requests

BASE_URL = 'http://localhost:5000/api/v1'


def createKnowledgeBase(assistantName):
    url = f'{BASE_URL}/knowledge-base/{assistantName}'
    response = requests.post(url, '''docFilePath''')  # TODO get docFilePath by assistantName
    return response


def initSession(assistantName):
    url = f'{BASE_URL}/llm/{assistantName}'
    response = requests.post(url, '''promptFilePath''')   #TODO get promptFilePath by assistantName
    return response

def sendCoreChat(assistantName, payload):
    url = f'{BASE_URL}/llm/query/{assistantName}'
    response = requests.post(url, payload)
    return response


def closeSession(assistantName):
    url = f'{BASE_URL}/llm/{assistantName}'
    response = requests.delete(url)
    return response

