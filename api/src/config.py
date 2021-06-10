from pydantic import BaseSettings


class Settings(BaseSettings):
    kafka_topics: list[str] = []
    kafka_hosts: list[str] = []
    database_url: str
    movie_api_url: str
    log_level: str = "INFO"
    jwt_public_key: str
    jwt_algorithm: str = "RS256"

    @property
    def kafka_hosts_as_string(self):
        return ",".join(self.kafka_hosts)


settings = Settings()
