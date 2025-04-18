from celery import Celery
from datetime import datetime, timedelta
from app.db.database import SessionLocal
from app.models.product import Product
from celery.schedules import crontab

# Initialize Celery
celery_app = Celery(
    "inventory_system",
    broker="redis://localhost:6379/0",  # Redis as the message broker
    backend="redis://localhost:6379/0",  # Redis for storing results
)

# Task to scan inventory and apply pricing rules
@celery_app.task
def scan_inventory():
    db = SessionLocal()
    products = db.query(Product).all()
    for product in products:
        # Apply price adjustment for products nearing expiration (7 days)
        if product.expiration_date <= datetime.utcnow() + timedelta(days=7):
            product.price = product.price * 0.9  # 10% discount for near-expiry items
    db.commit()
    db.close()
    return {"message": "Inventory scanned and price adjustments applied"}

# Task to trigger low-stock alerts
@celery_app.task
def trigger_low_stock_alert():
    db = SessionLocal()
    low_stock_products = db.query(Product).filter(Product.stock <= 5).all()
    # You can replace this with a real alert system (e.g., email, push notifications)
    for product in low_stock_products:
        print(f"Low stock alert: Product {product.name}, Stock: {product.stock}")
    db.close()
    return {"message": "Low stock alerts triggered"}

# Periodic task schedule configuration
celery_app.conf.beat_schedule = {
    "scan-inventory-every-hour": {
        "task": "app.celery_worker.scan_inventory",
        "schedule": timedelta(hours=1),  # Run every hour
    },
    "low-stock-alert-every-hour": {
        "task": "app.celery_worker.trigger_low_stock_alert",
        "schedule": timedelta(hours=1),  # Run every hour
    },
    'check-low-stock-every-day': {
        'task': 'app.tasks.low_stock_alert.check_low_stock_alerts',
        'schedule': crontab(minute=0, hour=0),  # Runs every day at midnight
    },
    "adjust-dynamic-prices-daily": {
        "task": "app.tasks.dynamic_pricing.apply_dynamic_pricing",
        "schedule": crontab(hour=0, minute=0),  # Every midnight
    }
}

celery_app.conf.timezone = "UTC"
celery_app.autodiscover_tasks(['app.tasks'])
