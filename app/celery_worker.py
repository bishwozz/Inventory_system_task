from celery import Celery
import os
from dotenv import load_dotenv
from celery.schedules import crontab

# Load environment variables
load_dotenv()

# Celery app configuration
app = Celery('worker', broker=os.getenv('CELERY_BROKER_URL'), backend=os.getenv('CELERY_RESULT_BACKEND'))

# Automatically discover tasks in the tasks module
app.conf.imports = ('app.tasks.celery_notifications',)

# Celery worker starts with:
# celery -A celery_worker.app worker --loglevel=info

# Schedule tasks to run periodically (every day)
from celery import Celery
from celery.schedules import crontab

app = Celery('worker', broker='redis://redis_cache:6379/0')

# Define periodic task schedule
app.conf.beat_schedule = {
    'check-low-stock-products': {
        'task': 'app.tasks.low_stock_alert.check_low_stock_products',
        'schedule': crontab(minute=0, hour=0),  # Run once a day at midnight
    },
    'update-product-prices': {
        'task': 'app.tasks.update_product_prices',
        'schedule': crontab(minute=0, hour=0),  # Runs every day at midnight
    },
    'check-expiring-products': {
        'task': 'app.tasks.expiration_alert.check_expiring_products',
        'schedule': crontab(minute=0, hour=0),  # Run once a day at midnight
    },
}

