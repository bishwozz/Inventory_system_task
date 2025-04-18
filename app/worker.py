from celery import Celery
from app.core.config import settings  # Import settings for Redis URL

celery_app = Celery(
    "worker",
    broker=settings.REDIS_URL,  # Use Redis URL from the environment
    backend=settings.REDIS_URL
)

celery_app.conf.timezone = "UTC"
celery_app.conf.task_default_retry_delay = 60  # Retry delay in seconds
celery_app.conf.task_max_retries = 5  # Max retries