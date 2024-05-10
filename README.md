# Orquestradora-LabDeIA

This project utilizes Flask, a Python microframework, to create a web application for managing assistants, chats, and documents for a project by Creath Digital. Here's a brief overview of the project structure and functionalities:

## Project Structure

The project is organized into three main sections: routes, models, and database interaction.

### Routes
- **Assistants**: Contains routes for managing assistant-related operations.
- **Chats**: Includes routes for handling chat-related functionalities.
- **Documents**: Consists of routes for managing document-related operations.

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

- **DocumentType Enum**: The type of document is defined by an enum called DocumentType, which has two values: "rag" or "prompt".
- **File Storage**: Document files are saved within the project folder, and only the file path is stored in the database.

## Setup Instructions

To set up the project locally, follow these steps:

1. Clone the repository.
2. Install the required dependencies using pip: `pip install -r requirements.txt`.
3. Configure the MongoDB connection details in the Flask application.
4. Run the Flask application: `python main.py`.

## Contributing

If you'd like to contribute to this project, feel free to fork the repository and submit a pull request with your changes.

## License

This project is licensed under the [MIT License](LICENSE).
