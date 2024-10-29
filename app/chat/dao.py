from typing import List

from sqlalchemy import select, or_, and_

from app.chat.models import Message
from app.dao.base import BaseDAO
from app.database import async_session_maker


class MessagesDAO(BaseDAO):
    model = Message

    @classmethod
    async def get_messages(cls, sender_id: int, recipient_id: int) -> List[Message]:
        async with async_session_maker() as session:
            query = select(cls.model).filter(
                or_(
                    and_(cls.model.sender_id == sender_id, cls.model.recipient_id == recipient_id),
                    and_(cls.model.sender_id == recipient_id, cls.model.recipient_id == sender_id)
                )
            ).order_by(cls.model.created_at)
            result = await session.execute(query)
            return result.scalars().all()
