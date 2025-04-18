import os
from celery import Celery
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

# Load secret from environment
REDIS_URL = os.getenv("REDIS_URL")

# Create a Celery instance
celery_app = Celery('inventory_system', broker=REDIS_URL)

celery_app.conf.result_backend = REDIS_URL
