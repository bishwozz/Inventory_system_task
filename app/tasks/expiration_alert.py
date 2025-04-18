from celery import Celery
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models import Product
from datetime import datetime, timedelta
import logging
from celery_worker import app

# Setup logging for notifications
logging.basicConfig(level=logging.INFO)

# Expiration threshold (e.g., products expiring in the next 3 days)
EXPIRATION_THRESHOLD_DAYS = 3

# Task to check for expiring products
@app.task
def check_expiring_products():
    db: Session = next(get_db())  # Get DB session

    # Get the current date
    current_date = datetime.now()

    # Query to find products expiring within the threshold
    expiring_products = db.query(Product).filter(Product.expiration_date <= current_date + timedelta(days=EXPIRATION_THRESHOLD_DAYS)).all()

    if expiring_products:
        for product in expiring_products:
            # Log or send notification about product expiration
            logging.info(f"Expiration alert: Product '{product.name}' is expiring on {product.expiration_date}!")
    else:
        logging.info("No products are nearing expiration.")
