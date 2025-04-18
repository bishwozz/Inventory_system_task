from celery import shared_task
from app.models import Product
from app.db.database import SessionLocal
from datetime import datetime, timedelta
import logging

# Configure logger
logger = logging.getLogger(__name__)

# Mock Notification Function
def send_notification(message: str):
    logger.info(f"Sending notification: {message}")
    return message

@shared_task
def check_expiring_products():
    # Get the current date and the date 30 days from now
    today = datetime.utcnow()
    expiration_threshold = today + timedelta(days=30)

    # Fetch products expiring soon
    db = SessionLocal()
    expiring_products = db.query(Product).filter(Product.expiry_date <= expiration_threshold).all()

    if expiring_products:
        for product in expiring_products:
            message = f"Product {product.name} is expiring soon. Expiry date: {product.expiry_date}."
            send_notification(message)
    else:
        logger.info("No products expiring soon.")
    db.close()

@shared_task
def check_low_stock_products():
    # Fetch low-stock products (for example, stock < 5)
    db = SessionLocal()
    low_stock_products = db.query(Product).filter(Product.stock < 5).all()

    if low_stock_products:
        for product in low_stock_products:
            message = f"Product {product.name} is low in stock. Current stock: {product.stock}."
            send_notification(message)
    else:
        logger.info("No products with low stock.")
    db.close()
