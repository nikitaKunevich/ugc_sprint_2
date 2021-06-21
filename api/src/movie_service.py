"""МОдуль для взаимодействия с сервисом MovieApi."""
from contextlib import asynccontextmanager
from typing import Optional

import backoff
from config import settings
from httpx import AsyncClient, HTTPError


@asynccontextmanager
async def get_service(authorization):
    """Возвращает MovieService."""
    service = MovieService(authorization)
    yield service
    await service.close()


class MovieService:
    """Сервис для работы с MovieApi."""

    def __init__(self, authorization):
        self._client = AsyncClient(
            base_url=settings.movie_api_url,
            headers={"Authorization": f"{authorization}"},
        )

    @backoff.on_exception(backoff.expo, HTTPError, max_time=60, max_value=10)
    async def get_movie(self, movie_id) -> Optional[dict]:
        """Возвращает информацию о фильме по идентификатору."""
        resp = await self._client.get(f"/v1/film/{movie_id}")
        if resp.status_code == 404:
            return None
        return resp.json()

    async def close(self):
        """Завершает работу сервиса."""
        await self._client.aclose()
