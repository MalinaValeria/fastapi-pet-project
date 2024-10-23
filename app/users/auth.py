from datetime import timedelta, datetime, timezone

from jose import jwt
from passlib.context import CryptContext

from app.config import get_auth_data, settings
from app.users.dao import UsersDAO
from app.users.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(email: str, password: str) -> User | None:
    user = await UsersDAO.find_one_or_none(email=email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(hours=settings.ACCESS_TOKEN_EXPIRES)
    to_encode.update({"exp": expire})
    auth_data = get_auth_data()
    encoded_jwt = jwt.encode(to_encode, auth_data['key'], algorithm=auth_data['algorithm'])
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRES)
    to_encode.update({"exp": expire})
    auth_data = get_auth_data()
    encoded_jwt = jwt.encode(to_encode, auth_data['key'], algorithm=auth_data['algorithm'])
    return encoded_jwt
