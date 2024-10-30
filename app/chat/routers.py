from datetime import datetime
from typing import List, Dict

from fastapi import APIRouter, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.websockets import WebSocket
from fastapi.websockets import WebSocketDisconnect

from app.chat.dao import MessagesDAO
from app.chat.schemas import MessageRead, MessageCreate
from app.users.dependensies import get_current_user
from app.users.models import User

templates = Jinja2Templates(directory='app/templates')
router = APIRouter(tags=['Chat'])


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: int):
        self.active_connections.pop(user_id)

    async def send_message(self, message: dict, user_id: int):
        try:
            websocket = self.active_connections[user_id]
            await websocket.send_json(message)
        except KeyError:
            pass

    async def broadcast(self, message: dict):
        for index, connection in self.active_connections.items():
            await connection.send_json(message)


manager = ConnectionManager()


@router.get('/', response_class=HTMLResponse, summary='Chat')
async def get_chat_page(request: Request, user_data: User = Depends(get_current_user)):
    return templates.TemplateResponse('chat.html', context={'request': request, 'user': user_data})


@router.websocket('/ws/{user_id}')
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast({'message': data, 'user_id': user_id})
    except WebSocketDisconnect:
        manager.disconnect(user_id)


@router.get('/messages/{interlocutor_id}', response_model=List[MessageRead])
async def get_messages(interlocutor_id: int, user: User = Depends(get_current_user)):
    return await MessagesDAO.get_messages(user.id, interlocutor_id)


@router.post('/messages/', response_model=MessageCreate)
async def send_message(message: MessageCreate, user: User = Depends(get_current_user)):
    await MessagesDAO.add(
        sender=user.id,
        recipient=message.recipient,
        content=message.content
    )
    message_data = {
        'sender': user.id,
        'recipient': message.recipient,
        'content': message.content,
        'created_at': datetime.now().isoformat()
    }

    await manager.send_message(message_data, message.recipient)
    await manager.send_message(message_data, user.id)

    return {'recipient': message.recipient, 'content': message.content, 'msg': 'Message sent'}
