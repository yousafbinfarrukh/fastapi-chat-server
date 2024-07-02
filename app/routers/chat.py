from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from ..services.connection_manager import ConnectionManager
from ..services.auth_service import decode_access_token

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
            await manager.broadcast(f"{username} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket, username)
        await manager.broadcast(f"{username} disconnected")
