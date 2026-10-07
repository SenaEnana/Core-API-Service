from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Core API Service"
    VERSION: str = "0.1.0"
    API_PREFIX: str = "/api/v1"
    DEBUG: bool = True
    ALLOWED_ORIGINS: list[str] = ["http://localhost:3000"]
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str

    model_config = SettingsConfigDict(env_file=".env")

    class Config:
        env_file = ".env"

settings = Settings()
