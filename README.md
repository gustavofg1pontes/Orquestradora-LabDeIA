# Orquestradora-LabDeIA

This project utilizes Flask, a Python microframework, to create a web application for managing assistants, chats, and
documents for a project by Creath Digital. Here's a brief overview of the project structure and functionalities:

## Project Structure

The project is organized into three main sections: routes, models, and database interaction.

### Routes

#### Assistants

- **POST /assistants/add**: Add a new assistant.
  ```json
  request:
  {
    "name": "Assistant Name",
    "owner_id": "Owner id"
  }
- **GET /assistants/list**: List all assistants.
  ```json
  response:
  [
    {
      "_id": "id",
      "name": "Assistant Name",
      "company": "Company Name",
      "createdAt": "2021-09-01T00:00:00"
    }
  ]
- **GET /assistants/get/&lt;id&gt;**: Get details of a specific assistant.
  ```json
  response:
  {
    "_id": "id",
    "name": "Assistant Name",
    "company": "Company Name",
    "createdAt": "2021-09-01T00:00:00"
  }
- **PUT /assistants/update/&lt;id&gt;**: Update details of a specific assistant.
  ```json
  request:
  {
    "name": "Assistant Name",
    "company": "Company Name"
    "createdAt": "2021-09-01T00:00:00"
  }
- **DELETE /assistants/delete/&lt;id&gt;**: Delete a specific assistant.

#### Chats

- **POST /chats/enviarMensagemLLM**: Send a message to LLM.
    ```json
    request:
    {
      "id": "+5513988593464",
      "message_service": "Whatsapp",
      "username": "nome",
      "assistant_id": "id",
      "active": true,
      "message": "mensagem do usuario"
    }
- **GET /chats/get/&lt;id&gt;**: Get details of a specific chat.
  ```json
  response:
  {
    "_id": "id",
    "channel": {
      "id": "+551300000000",
      "message_service": "Whatsapp"
    },
    "username": "nome",
    "assistant_id": "id",
    "active": true,
    "message": "mensagem do Usuario",
    "response": "resposta LLM",
    "createdAt": "05-09-2024T19:57:00"
  }
- **GET /chats/list**: List all chats.
  ```json
    response:
    [
        {
        "_id": "id",
        "channel": {
            "id": "+551300000000",
            "message_service": "Whatsapp"
        },
        "username": "nome",
        "assistant_id": "id",
        "active": true,
        "message": "mensagem do Usuario",
        "response": "resposta LLM",
        "createdAt": "05-09-2024T19:57:00"
        }
    ]
- **GET /chats/listarAtivos**: List all active chats.
  ```json
    response:
    [
        {
        "_id": "id",
        "channel": {
            "id": "+551300000000",
            "message_service": "Whatsapp"
        },
        "username": "nome",
        "assistant_id": "id",
        "active": True,
        "message": "mensagem do Usuario",
        "response": "resposta LLM",
        "createdAt": "05-09-2024T19:57:00"
        }
    ]
- **GET /chats/listarInativos**: List all inactive chats.
  ```json
    response:
    [
        {
        "_id": "id",
        "channel": {
            "id": "+551300000000",
            "message_service": "Whatsapp"
        },
        "username": "nome",
        "assistant_id": "id",
        "active": False,
        "message": "mensagem do Usuario",
        "response": "resposta LLM",
        "createdAt": "05-09-2024T19:57:00"
        }
    ]
- **PUT /chats/desativar/&lt;id&gt;**: Deactivate a specific chat.
- **PUT /chats/ativar/&lt;id&gt;**: Activate a specific chat.

#### Documents

- **POST /documents/add**: Upload a new document.
    ```json
    request form-data:
    {
        "file": "file attached"
        "type": "rag or prompt",
        "assistant_id": "id",
    }
- **GET /documents/list**: List all documents.
  ```json
    response:
    [
        {
        "_id": "id",
        "filepath": "file path",
        "filename": "file name",
        "type": "rag or prompt",
        "assistant_id": "id",
        "createdAt": "2021-09-01T00:00:00"
        }
    ]
- **GET /documents/get/&lt;id&gt;**: Get details of a specific document.
  ```json
    response:
    {
          "_id": "id",
        "filepath": "file path",
        "filename": "file name",
        "type": "rag or prompt",
        "assistant_id": "id",
        "createdAt": "2021-09-01T00:00:00"
    }
- **PUT /documents/path/get/&lt;id&gt;**: Get the file path of a specific document.
- **GET /documents/download/&lt;id&gt;**: Download a specific document.
- **DELETE /documents/delete/&lt;id&gt;**: Delete a specific document.

##### The documents folder architecture is:

    Orquestradora-LabDeIA
      └── documents
          ├── <assistant id>
          │   ├── knowledge
          │   │   └── rag.md
          │   └── prompt.txt
          │   
          └── <assistant id>
              ├── knowledge
              │   └── rag.md
              └── prompt.txt

#### Auth

- **POST /auth/login**: Login to the application.
    ```json
    request:
    {
        "email": "user email",
        "password": "password"
    }
    response:
    {
        "token": "access token",
        "user": {
            "email": "user email",
            "id": "id",
            "name": "name"
        }
    }
- **POST /auth/register**: Register a new user.
    ```json
    request:
    {
        "name": "name"
        "email": "user email",
        "password": "password",
    }

### Models

- **Assistant Model**:
    - Attributes: name, company, createdAt
- **Chat Model**:
    - Attributes: channel (id and message_service), username, assistant_id, active, message, response, createdAt
- **Document Model**:
    - Attributes: filepath, filename, type (rag or prompt), assistant_id, createdAt

### Database Interaction

The project utilizes MongoDB as the database. Each model corresponds to a collection in the MongoDB database.

## Additional Information

- **DocumentType Enum**: The type of document is defined by an enum called DocumentType, which has two values: "rag"
  or "prompt".
- **File Storage**: Document files are saved within the project folder, and only the file path is stored in the
  database.

## Setup Instructions

To set up the project locally, follow these steps:

1. Clone the repository.
2. Run `cp .env.example .env` to create a new `.env` file and set it up using your mongodb connection url.
3. Install the required dependencies using pip: `pip install -r requirements.txt`.
4. Run the Flask application on waitress running: `waitress-serve --port=8080 --call main:create_app`.

## Contributing

If you'd like to contribute to this project, feel free to fork the repository and submit a pull request with your
changes.

## License

This project is licensed under the [MIT License](LICENSE).
