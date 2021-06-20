"""Middlewares для API."""
import logging

import jwt
from config import settings
from jwt import PyJWTError
from starlette.authentication import (
    AuthCredentials,
    AuthenticationBackend,
    AuthenticationError,
    BaseUser,
)


class User(BaseUser):
    """Класс пользователя."""

    def __init__(self, user_id: str) -> None:
        self.user_id = user_id

    @property
    def is_authenticated(self) -> bool:
        """Признак авторизации пользователя."""
        return True

    @property
    def display_name(self) -> str:
        """Отображаемое имя пользователя."""
        return f"user_id={self.user_id}"


class JWTAuthBackend(AuthenticationBackend):
    """Класс для работы с авторизацией."""

    async def authenticate(self, request):
        """Авторизация пользователя."""
        # Get JWT token from user's cookies

        if "Authorization" not in request.headers:
            logging.debug("no auth")
            return

        auth = request.headers["Authorization"]
        try:
            scheme, token = auth.split()
            if scheme.lower() != "bearer":
                logging.debug("not bearer auth")
                return
        except ValueError:
            logging.debug(f"Invalid authorization header: {auth}")
            raise AuthenticationError("Invalid authorization")

        # Returns UnauthenticatedUser if token does not exists in header
        if not token:
            logging.debug("no token")
            return

        # Checks the validity of the JWT token, if token is invalid returns UnauthenticatedUser object
        try:
            jwt_decoded = jwt.decode(
                token,
                settings.jwt_public_key,
                algorithms=[settings.jwt_algorithm],
            )
        except PyJWTError as err:
            logging.error(str(err))
            logging.exception("invalid token, user is unauthenticated")
            raise AuthenticationError("Invalid credentials")

        # In case if token is valid returns an object of the authorized user
        permissions = jwt_decoded["permissions"]

        logging.debug(
            f"token is valid, user: {jwt_decoded['sub']} permissions: {permissions}, jwt: {jwt_decoded}",
        )
        return AuthCredentials(permissions), User(user_id=jwt_decoded["sub"])
