from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)


class Friends(Base):
    __tablename__ = 'friends'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    friend: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
