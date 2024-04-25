from functools import lru_cache

from pydantic import PostgresDsn, validator
from pydantic_settings import BaseSettings
from dotenv import load_dotenv


class Settings(BaseSettings):
    DEBUG: bool

    load_dotenv()

    HOST: str
    
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    SQLALCHEMY_URL: str | None = None

    @validator('POSTGRES_HOST', pre=True)
    def set_db_host(cls, value, values):
        if values.get("DEBUG"):
            if values.get("HOST") == '0.0.0.0':
                return 'localhost'
            return values.get("HOST")
        return value

    @validator('SQLALCHEMY_URL', pre=True)
    def get_sqlalchemy_url(cls, value, values):
        if isinstance(value, str):
            return value

        return str(PostgresDsn.build(
            scheme='postgresql+asyncpg',
            username=values.get('POSTGRES_USER'),
            password=values.get('POSTGRES_PASSWORD'),
            host=values.get('POSTGRES_HOST'),
            port=values.get('POSTGRES_PORT'),
            path=values.get("POSTGRES_DB")
        ))


@lru_cache
def get_settings() -> Settings:
    return Settings()
