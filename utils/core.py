import requests

BASE_URL = 'http://<core-url>/api/v1'    #TODO: Change this to the core URL


def create_knowledge_base(assistant_id):
    url = f'{BASE_URL}/knowledge-base/{assistant_id}'
    rag_path = f'./documents/{assistant_id}/knowledge/rag.md'
    response = requests.post(url, rag_path)
    return response


def send_core_chat(assistant_id, payload):
    url = f'{BASE_URL}/llm/{assistant_id}/query'
    response = requests.post(url, payload)
    return response
