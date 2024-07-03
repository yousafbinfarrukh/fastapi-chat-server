from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from ..services.connection_manager import ConnectionManager
from ..services.auth_service import decode_access_token, encrypt_message, decrypt_message, get_current_user
from ..services.group_manager import group_manager
from ..database import get_db
from ..models import User, Group

router = APIRouter()

manager = ConnectionManager()

async def get_current_user_ws(websocket: WebSocket):
    token = websocket.query_params.get("token")
    username = decode_access_token(token)
    if not username:
        await websocket.close(code=1008)
        raise WebSocketDisconnect(code=1008)
    return username

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, db: Session = Depends(get_db)):
    username = await get_current_user_ws(websocket)
    await manager.connect(websocket, username)
    user = db.query(User).filter(User.username == username).first()
    user_id = user.id

    # Send personal chat history
    personal_messages = manager.get_chat_history(user_id, db)
    for message in personal_messages:
        await websocket.send_text(f"{message.sender.username}: {message.content}")

    # Send group chat history
    group_memberships = user.group_memberships
    for membership in group_memberships:
        group_id = membership.group_id
        group_messages = manager.get_group_chat_history(group_id, db)
        for message in group_messages:
            await websocket.send_text(f"[{membership.group.name}] {message.sender.username}: {message.content}")

    try:
        while True:
            data = await websocket.receive_text()
            message_data = data.split(":", 2)
            if len(message_data) == 3:
                recipient_type, recipient, message = message_data
                encrypted_message = encrypt_message(f"{username}: {message}")
                if recipient_type == "user":
                    await manager.send_personal_message(encrypted_message, recipient.strip(), db)
                elif recipient_type == "group":
                    members = group_manager.get_group_members(recipient.strip())
                    for member in members:
                        await manager.send_personal_message(encrypted_message, member, db)
                    manager.save_group_message(recipient.strip(), encrypted_message, db)
                else:
                    await manager.send_personal_message("Invalid recipient type. Use 'user: username: message' or 'group: groupname: message'", username)
            else:
                await manager.send_personal_message("Invalid message format. Use 'recipient_type: recipient: message'", username)
    except WebSocketDisconnect:
        manager.disconnect(websocket, username)
        await manager.broadcast(f"{username} disconnected")
