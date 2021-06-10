import logging

import backoff
from config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

logger = logging.getLogger(__name__)


engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def init_db():
    logger.debug("creating tables")

    @backoff.on_exception(backoff.constant, Exception, interval=5)
    def create_tables():
        Base.metadata.create_all(bind=engine)

    create_tables()
