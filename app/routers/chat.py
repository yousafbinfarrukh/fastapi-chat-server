from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from ..services.connection_manager import ConnectionManager
from ..services.auth_service import decode_access_token, encrypt_message, decrypt_message
from ..services.group_manager import group_manager

router = APIRouter()

manager = ConnectionManager()

async def get_current_user(websocket: WebSocket):
    token = websocket.query_params.get("token")
    username = decode_access_token(token)
    if not username:
        await websocket.close(code=1008)
        raise WebSocketDisconnect(code=1008)
    return username

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    username = await get_current_user(websocket)
    await manager.connect(websocket, username)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = data.split(":", 2)
            if len(message_data) == 3:
                recipient_type, recipient, message = message_data
                encrypted_message = encrypt_message(f"{username}: {message}")
                if recipient_type == "user":
                    await manager.send_personal_message(encrypted_message, recipient.strip())
                elif recipient_type == "group":
                    members = group_manager.get_group_members(recipient.strip())
                    for member in members:
                        await manager.send_personal_message(encrypted_message, member)
                else:
                    await manager.send_personal_message("Invalid recipient type. Use 'user: username: message' or 'group: groupname: message'", username)
            else:
                await manager.send_personal_message("Invalid message format. Use 'recipient_type: recipient: message'", username)
    except WebSocketDisconnect:
        manager.disconnect(websocket, username)
        await manager.broadcast(f"{username} disconnected")
