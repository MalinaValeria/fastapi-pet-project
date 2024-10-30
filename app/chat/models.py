from sqlalchemy import Integer, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Message(Base):
    __tablename__ = 'messages'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sender: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    recipient: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    content: Mapped[str] = mapped_column(Text)
