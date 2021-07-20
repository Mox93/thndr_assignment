from functools import lru_cache

from pydantic import AnyUrl, BaseSettings, Field, HttpUrl


class Settings(BaseSettings):
    pg_dsn: AnyUrl = Field(..., env="DATABASE_URL")
    mqtt_topic: str
    mqtt_host: str
    mqtt_port: int
    api_url: HttpUrl

    class Config:
        env_file = '.env.dev'
        env_file_encoding = 'utf-8'


@lru_cache()
def settings(env_file=None) -> Settings:
    return Settings(_env_file=env_file) if env_file else Settings()
