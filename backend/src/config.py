from pydantic import PostgresDsn
from pydantic_settings import BaseSettings

class Config(BaseSettings):
    AUTH_JWT_ALG: str
    AUTH_JWT_SECRET: str
    AUTH_JWT_EXP: int = 5  # minutes

    DB_URL: PostgresDsn
    DB_URL_TEST: PostgresDsn

    class Config:
        env_file = ".env"


settings = Config()