from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Inventory System"
    VERSION: str = "1.0.0"
    DATABASE_URL: str
    REDIS_URL: str

    class Config:
        env_file = ".env"

settings = Settings()
