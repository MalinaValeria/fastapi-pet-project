from fastapi import APIRouter, Response, Depends
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from fastapi.requests import Request
from fastapi.responses import HTMLResponse

from app.config import settings, get_auth_data
from app.exceptions import UserAlreadyExistsException, PasswordMismatchException, IncorrectEmailOrPasswordException, \
    NoJwtException, NoUserIdException
from app.users.auth import get_password_hash, authenticate_user, create_access_token, create_refresh_token
from app.users.dao import UsersDAO
from app.users.schemas import SUserRegister
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory='app/templates')
router = APIRouter(prefix='/auth', tags=['Auth'])
ACCESS_TOKEN_EXPIRES = settings.ACCESS_TOKEN_EXPIRES
REFRESH_TOKEN_EXPIRES = settings.REFRESH_TOKEN_EXPIRES


def set_cookies(response: Response, key: str, value: str, token_age: int):
    response.set_cookie(key=key, value=value, max_age=token_age * 60,
                        expires=token_age * 60, path='/', domain=None, secure=False, httponly=True,
                        samesite='lax')


@router.get('/registration/', response_class=HTMLResponse, summary='Registration')
async def get_registration_page(request: Request):
    return templates.TemplateResponse('registration.html', context={'request': request})


@router.post('/registration/')
async def register(user_data: SUserRegister) -> dict:
    user = await UsersDAO.find_one_or_none(email=user_data.email)
    if user:
        raise UserAlreadyExistsException

    if user_data.password != user_data.password_confirm:
        raise PasswordMismatchException
    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add(
        name=user_data.name,
        email=user_data.email,
        hashed_password=hashed_password
    )

    return {'message': 'User created successfully'}


@router.get('/login/', response_class=HTMLResponse, summary='Login')
async def get_login_page(request: Request):
    return templates.TemplateResponse('login.html', context={'request': request})


@router.post('/login/')
async def login(response: Response, form: OAuth2PasswordRequestForm = Depends()) -> dict:
    user = await authenticate_user(email=form.username, password=form.password)
    if not user:
        raise IncorrectEmailOrPasswordException

    access_token = create_access_token(data={'sub': str(user.id)})
    refresh_token = create_refresh_token(data={'sub': str(user.id)})

    set_cookies(response, key='access_token', value=access_token, token_age=ACCESS_TOKEN_EXPIRES)
    set_cookies(response, key='refresh_token', value=refresh_token, token_age=REFRESH_TOKEN_EXPIRES)
    set_cookies(response, key='logged_in', value='True', token_age=ACCESS_TOKEN_EXPIRES)

    return {'access_token': access_token, 'refresh_token': refresh_token}


@router.post('/refresh/')
def refresh_jwt(response: Response, refresh_token: str) -> dict:
    try:
        auth_data = get_auth_data()
        payload = jwt.decode(refresh_token, auth_data['key'], algorithms=[auth_data['algorithm']])
        user_id = payload.get('sub')
        if not user_id:
            raise NoUserIdException
        new_access_token = create_access_token(data={'sub': user_id})
        set_cookies(response, key='access_token', value=new_access_token, token_age=ACCESS_TOKEN_EXPIRES)
        set_cookies(response, key='logged_in', value='True', token_age=ACCESS_TOKEN_EXPIRES)
        return {'access_token': new_access_token}

    except JWTError:
        raise NoJwtException


@router.post('/logout/')
def logout(response: Response):
    response.delete_cookie(key='access_token')
    return {'status': 'success'}
