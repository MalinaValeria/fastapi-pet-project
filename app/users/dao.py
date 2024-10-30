from sqlalchemy import select, or_, outerjoin
from typing import List, Optional, Dict

from sqlalchemy.orm import selectinload

from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.users.models import User, Friends


class UsersDAO(BaseDAO):
    model = User

    @classmethod
    async def find_by_email_or_username(cls, identifier: str) -> Optional[User]:
        async with async_session_maker() as session:
            query = or_(cls.model.email == identifier, cls.model.username == identifier)
            result = await session.execute(select(cls.model).where(query))
            return result.scalar_one_or_none()

    @classmethod
    async def find_usernames_by_substring(cls, substring: str) -> List[User]:
        async with async_session_maker() as session:
            query = select(cls.model).where(cls.model.username.ilike(f'%{substring}%'))
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def get_all_friends(cls, user_id: int) -> List[Dict[str, int | str]]:
        async with async_session_maker() as session:
            friends_table = Friends.__table__.alias('friends')
            users_table = cls.model.__table__.alias('users')

            query = (
                select(users_table.c.id, users_table.c.username)
                .select_from(
                    outerjoin(
                        users_table,
                        friends_table,
                        users_table.c.id == friends_table.c.friend
                    )
                )
                .filter(friends_table.c.user == user_id)
            )

            result = await session.execute(query)
            return [{"id": row.id, "username": row.username} for row in result]


class FriendsDAO(BaseDAO):
    model = Friends
