import logging
from typing import Optional

from logstash_async.handler import AsynchronousLogstashHandler
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware

import movie_service
from config import settings
from confluent_kafka.cimpl import KafkaException
from db import SessionLocal, init_db
from db_service import DbService, service_with_session
from fastapi import Depends, FastAPI, HTTPException
from fastapi.params import Body
from kafka import AIOProducer, create_topics
from middlewares import JWTAuthBackend
from schemas import Event
from starlette.requests import Request

import sentry

logger = logging.getLogger(__name__)
logging.basicConfig(level=settings.log_level)

app = FastAPI(
    title="UGC API",
    docs_url="/swagger",
    openapi_url="/swagger.json",
)
app.add_middleware(AuthenticationMiddleware, backend=JWTAuthBackend())
app.add_middleware(SentryAsgiMiddleware)

producer: Optional[AIOProducer] = None


@app.on_event("startup")
def startup_event():
    global producer
    producer = AIOProducer()
    producer.start()
    create_topics()

    uvicorn_logger = logging.getLogger()
    handler = AsynchronousLogstashHandler(settings.logstash_host, settings.logstash_port, transport='logstash_async.transport.UdpTransport',
                                          database_path='logstash.db')
    uvicorn_logger.addHandler(handler)

    init_db()


@app.on_event("shutdown")
async def shutdown_event():
    producer.close()


def get_db() -> DbService:
    with service_with_session(SessionLocal()) as service:
        yield service


async def get_movie_service(request: Request) -> movie_service.MovieService:
    async with movie_service.get_service(
        request.headers.get("Authorization")
    ) as service:
        yield service


@app.post("/collect", description="Сохраняет аналитические запросы", status_code=204)
async def create_item(request: Request, event: Event):
    try:
        await producer.produce("events", event.dict())
    except KafkaException as exc:
        logger.exception(exc)
    return {}


@app.post(
    "/movie/{movie_id}/likes", description="Лайкнуть/дизлайкнуть фильм", status_code=204
)
async def like_movie(
    request: Request,
    movie_id: str,
    toggle: bool = Body(True, embed=True),
    db: DbService = Depends(get_db),
    movie_api=Depends(get_movie_service),
):
    if not request.user:
        raise HTTPException(status_code=401, detail="Only for authorized users")

    if not await movie_api.get_movie(movie_id):
        raise HTTPException(status_code=404, detail="Movie not found")
    db.toggle_movie_like(request.user.user_id, movie_id, toggle)
    return {}


@app.post(
    "/movie/{movie_id}/comments", description="Откомментировать фильм", status_code=204
)
async def comment(
    request: Request,
    movie_id: str,
    content: str = Body(..., embed=True),
    db: DbService = Depends(get_db),
    movie_api=Depends(get_movie_service),
):
    if not request.user:
        raise HTTPException(status_code=401, detail="Only for authorized users")
    if not await movie_api.get_movie(movie_id):
        raise HTTPException(status_code=404, detail="Movie not found")
    db.add_movie_comment(request.user.user_id, movie_id, content)
    return {}


@app.post(
    "/movie/{movie_id}/favourites",
    description="Отметить/снять метку фильма",
    status_code=204,
)
async def favourite_movie(
    request: Request,
    movie_id: str,
    toggle: bool = Body(True, embed=True),
    db: DbService = Depends(get_db),
    movie_api=Depends(get_movie_service),
):
    if not request.user:
        raise HTTPException(status_code=401, detail="Only for authorized users")

    if not await movie_api.get_movie(movie_id):
        raise HTTPException(status_code=404, detail="Movie not found")

    db.toggle_movie_favourite(request.user.user_id, movie_id, toggle)
    return {}
