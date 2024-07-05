# FastAPI Chat Application

This is a real-time chat application built with FastAPI, SQLAlchemy, and WebSockets. It supports user authentication, private messaging, group chats, and message encryption.

## Features

- User authentication (signup and login)
- Real-time private messaging
- Group chats
- Message encryption
- Persistent message storage with SQLAlchemy

## Requirements

- Python 3.10
- Docker (for deployment)
- AWS CLI (for deployment)

## Setup

### Clone the repository

```sh
git clone https://github.com/yourusername/chat-server.git
cd chat-server
```

### Create a virtual environment

```sh
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### Install dependencies

```sh
pip install -r requirements.txt
```

### Environment Variables

Generate encryption key and secret key using `generate_encryption_key.py` and `generate_secret_key.py`:

Create a `.env` file in the root directory and add the following environment variables:

```
SECRET_KEY=your_jwt_secret_key
ENCRYPTION_KEY=your_generated_encryption_key
```


### Initialize the Database

Run the following command to create the database tables:

```sh
python -m app.main
```

## Running the Application

### Run with Uvicorn

```sh
uvicorn app.main:app --reload
```

### Run with Docker

#### Build Docker Image

```sh
docker build -t chat-api .
```

#### Run Docker Container

```sh
docker run -it -p 8000:8000 chat-api
```

## API Endpoints

### Authentication

- **POST /signup**: Register a new user
- **POST /login**: Login a user

### WebSocket

- **/ws**: WebSocket endpoint for real-time chat

### Groups

- **POST /create_group**: Create a new group
- **POST /join_group**: Join a group
- **POST /leave_group**: Leave a group

## License

This project is licensed under the MIT License.