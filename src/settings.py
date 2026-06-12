from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    # database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5434/ads_db"
    jwt_secret: str = "change-me"
    jwt_algorithm: str = "HS256"
    kafka_bootstrap_servers: str = "localhost:9092"
    kafka_topic_ads: str = Field(
        default="ads",
        validation_alias="KAFKA_TOPIC_MARKETPLACE_ADS",
    )
    auth_service_url: str = "http://localhost:8000"

    database_url: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5434/ads_db",
        validation_alias="POSTGRES_CONNECTION_STRING",
    )

    @field_validator("database_url", mode="before")
    @classmethod
    def normalize_database_url(cls, v):
        if v is None:
            return v

        # если прилетело postgres:// или postgresql:// — нормализуем
        if isinstance(v, str):
            if v.startswith("postgres://"):
                return v.replace("postgres://", "postgresql+asyncpg://", 1)
            if v.startswith("postgresql://") and "+asyncpg" not in v:
                return v.replace("postgresql://", "postgresql+asyncpg://", 1)

        return v
