from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5434/ads_db"
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/ads_db"
    jwt_secret: str = "change-me"
    jwt_algorithm: str = "HS256"
    kafka_bootstrap_servers: str = "localhost:9092"
    kafka_topic_ads: str = "ads"
    auth_service_url: str = "http://localhost:8000"
