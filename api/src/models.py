"""Модуль содержит модели sqlalchemy."""
from uuid import uuid4

from db import Base
from sqlalchemy import Column, PrimaryKeyConstraint, String, Text


class Like(Base):
    """Лайки пользователей."""

    __tablename__ = "likes"
    user_id = Column(String, nullable=False)
    movie_id = Column(String, nullable=False)

    __table_args__ = (PrimaryKeyConstraint("user_id", "movie_id"),)


class Comment(Base):
    """Пользовательские комментарии."""

    __tablename__ = "comments"
    id = Column(String, unique=True, primary_key=True, default=str(uuid4()))
    user_id = Column(String, nullable=False)
    movie_id = Column(String, nullable=False)
    content = Column(Text, nullable=False)


class Favourite(Base):
    """Избранные фильмы пользователя."""

    __tablename__ = "favourites"
    user_id = Column(String, nullable=False)
    movie_id = Column(String, nullable=False)
    __table_args__ = (PrimaryKeyConstraint("user_id", "movie_id"),)
