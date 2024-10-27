from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class DatabaseConfig(BaseSettings):
    DATABASE_URL: PostgresDsn


database_settings = DatabaseConfig()