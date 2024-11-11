from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response

from app.users.dao import FriendsDAO, UsersDAO
from app.users.dependensies import get_current_user
from app.users.models import User
from app.users.schemas import SUserRead

router = APIRouter(prefix='/friends', tags=['Friends'])


@router.get('/', summary='Get friends')
async def get_friends(user_data: User = Depends(get_current_user)):
    friends = await UsersDAO.get_all_friends(user_data.id)
    return friends


@router.get('/search', response_model=List[SUserRead], summary='Find friend')
async def find_friend(username: str):
    users = await UsersDAO.find_usernames_by_substring(substring=username)
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with this username not found")
    return users


@router.post('/add/{friend_id}', summary='Add friend')
async def add_friend(friend_id: int, response: Response, user_id: User = Depends(get_current_user)):
    if not await UsersDAO.find_by_id(friend_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User(friend id) not found")
    await FriendsDAO.add(user=user_id.id, friend=friend_id)
    response.status_code = status.HTTP_201_CREATED
    return {'message': 'Friend added'}


@router.delete('/delete/{friend_id}', summary='Delete friend')
async def delete_friend(friend_id: int, response: Response, user_id: User = Depends(get_current_user)):
    await FriendsDAO.delete(user_id=user_id.id, friend_id=friend_id)
    response.status_code = status.HTTP_204_NO_CONTENT
    return {'message': 'Friend deleted'}
