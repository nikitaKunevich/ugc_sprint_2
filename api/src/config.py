"""Модуль настроек приложения."""
from typing import List

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Настройки приложения."""

    kafka_topics: List[str] = []
    kafka_hosts: List[str] = []
    database_url: str
    movie_api_url: str
    log_level: str = "INFO"
    jwt_public_key: str
    jwt_algorithm: str = "RS256"

    sentry_dsn: str
    environment: str = "local"

    logstash_host: str
    logstash_port: int

    @property
    def kafka_hosts_as_string(self):
        """Возвращает строку хостов Kafka через запятую."""
        return ",".join(self.kafka_hosts)


settings = Settings()
