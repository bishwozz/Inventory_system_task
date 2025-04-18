from pydantic import BaseSettings

class Settings(BaseSettings):

    DATABASE_URL: str
    REDIS_URL: str
    SECRET_KEY: str
    ALLOWED_ORIGINS: str

    class Config:
        env_file = ".env"

# Instantiate the settings
settings = Settings()
