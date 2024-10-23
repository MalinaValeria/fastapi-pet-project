from fastapi import APIRouter, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request

from app.users.dao import UsersDAO
from app.users.dependensies import get_current_user
from app.users.models import User

templates = Jinja2Templates(directory='app/templates')
router = APIRouter(tags=['Chat'])


@router.get('/', response_class=HTMLResponse, summary='Chat')
async def get_chat_page(request: Request, user_data: User = Depends(get_current_user)):
    all_users = await UsersDAO.find_all()
    return templates.TemplateResponse('chat.html', context={'request': request, 'user': user_data, 'users': all_users})
