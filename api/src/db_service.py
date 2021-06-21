"""Модуль для инкапсуляции работы с базой данных."""
from contextlib import contextmanager

import models
from sqlalchemy.orm import Session


@contextmanager
def service_with_session(session: Session):
    """Возвращает подготовленный сервис."""
    service = DbService(session)
    yield service
    service.close()


class DbService:
    """Сервис заключает в себе логику созранения взаимодействия пользователя с фильмом."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def close(self) -> None:
        """Завершает работу."""
        self._session.close()

    def toggle_movie_like(self, user_id, movie_id, toggle):
        """Создает запись в базе данных о лайке пользователя."""
        like = (
            self._session.query(models.Like)
            .filter_by(user_id=user_id, movie_id=movie_id)
            .one_or_none()
        )
        if toggle:
            if not like:
                like = models.Like(user_id=user_id, movie_id=movie_id)
                self._session.add(like)
        else:
            if like:
                self._session.delete(like)

        self._session.commit()

    def toggle_movie_favourite(self, user_id, movie_id, toggle):
        """СОздает запись об избранном фильме в базе данных."""
        favourite = (
            self._session.query(models.Favourite)
            .filter_by(user_id=user_id, movie_id=movie_id)
            .one_or_none()
        )
        if toggle:
            if not favourite:
                favourite = models.Favourite(user_id=user_id, movie_id=movie_id)
                self._session.add(favourite)
        else:
            if favourite:
                self._session.delete(favourite)

        self._session.commit()

    def add_movie_comment(self, user_id, movie_id, content):
        """Создает комментарий пользователя к фильму."""
        comment = models.Comment(user_id=user_id, movie_id=movie_id, content=content)
        self._session.add(comment)
        self._session.commit()
