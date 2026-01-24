"""Configuration file for the application."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabasePoolConfig(BaseSettings):
    """Configuration for the database pool."""
    pool_timeout: int = 30
    pool_recycle: int = 3600
    pool_pre_ping: bool = True


class DatabaseSettings(BaseSettings):
    """Configuration for the database."""
    host: str
    port: str
    user: str
    password: str
    database: str

    driver: str = "postgresql+asyncpg://"

    pool_config: DatabasePoolConfig = Field(default_factory=DatabasePoolConfig)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )
