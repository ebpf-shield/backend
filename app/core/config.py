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
    PORT: int
    HOST: str


class JwtSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
        env_prefix="JWT_",
    )

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int


settings = Settings()

jwt_settings = JwtSettings()
