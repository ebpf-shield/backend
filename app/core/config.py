from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )

    CONNECTION_STRING: str
    DB_NAME: str
    KAFKA_BROKERS: list[str]


settings = Settings()
