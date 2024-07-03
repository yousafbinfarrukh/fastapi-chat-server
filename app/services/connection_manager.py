from fastapi import WebSocket
from sqlalchemy.orm import Session
from typing import List, Dict
from ..database import get_db
from ..models import Message, GroupMessage, User, Group

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, username: str):
        await websocket.accept()
        self.active_connections[username] = websocket

    def disconnect(self, websocket: WebSocket, username: str):
        self.active_connections.pop(username, None)

    async def send_personal_message(self, message: str, recipient: str, db: Session):
        if recipient in self.active_connections:
            websocket = self.active_connections[recipient]
            await websocket.send_text(message)
        self.save_personal_message(recipient, message, db)

    async def broadcast(self, message: str):
        for connection in self.active_connections.values():
            await connection.send_text(message)

    def save_personal_message(self, recipient: str, message: str, db: Session):
        sender_username, message_content = message.split(": ", 1)
        sender = db.query(User).filter(User.username == sender_username).first()
        recipient_user = db.query(User).filter(User.username == recipient).first()
        db_message = Message(sender_id=sender.id, recipient_id=recipient_user.id, content=message_content)
        db.add(db_message)
        db.commit()

    def save_group_message(self, group_name: str, message: str, db: Session):
        sender_username, message_content = message.split(": ", 1)
        sender = db.query(User).filter(User.username == sender_username).first()
        group = db.query(Group).filter(Group.name == group_name).first()
        db_message = GroupMessage(sender_id=sender.id, group_id=group.id, content=message_content)
        db.add(db_message)
        db.commit()

    def get_chat_history(self, user_id: int, db: Session):
        messages = db.query(Message).filter(
            (Message.sender_id == user_id) | (Message.recipient_id == user_id)
        ).all()
        return messages

    def get_group_chat_history(self, group_id: int, db: Session):
        messages = db.query(GroupMessage).filter(
            GroupMessage.group_id == group_id
        ).all()
        return messages
