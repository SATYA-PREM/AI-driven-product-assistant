from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    MONGODB_URL: str
    MONGODB_DATABASE: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()