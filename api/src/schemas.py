"""Модуль содержит модели для валидации и отображения сущностей."""
from typing import Union

from pydantic import BaseModel


class MovieViewingHistoryPayload(BaseModel):
    """Полезная нагрузка о просмотре фильма."""

    movie_timestamp: int
    movie_id: str
    user_id: str


class Event(BaseModel):
    """Аналитическое событие в системе."""

    payload: Union[MovieViewingHistoryPayload]
    language: str
    timezone: str
    fingerprint: dict
    ip: str
    type: str
    version: str
