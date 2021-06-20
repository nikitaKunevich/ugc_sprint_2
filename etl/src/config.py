"""Модуль настроек приложения."""
from typing import List

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Настройки приложения."""

    message_wait_seconds: int
    message_batch_size: int
    kafka_consumer_group: str
    kafka_topics: List[str] = []
    kafka_hosts: List[str] = []
    clickhouse_main_host: str
    clickhouse_alt_hosts: List[str] = []

    @property
    def kafka_hosts_as_string(self):
        """Возвращает строку хостов Kafka через запятую."""
        return ",".join(self.kafka_hosts)

    @property
    def clickhouse_alt_hosts_as_string(self):
        """Возвращает строку хостов Clickhouse через запятую."""
        return ",".join(self.clickhouse_alt_hosts)


settings = Settings()
