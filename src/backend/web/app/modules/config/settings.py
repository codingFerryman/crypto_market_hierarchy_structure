from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    # DB
    pg_host: str
    pg_port: int
    pg_user: str

    class Config:
        env_file = ".env"
