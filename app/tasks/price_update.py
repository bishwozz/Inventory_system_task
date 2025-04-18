from celery import shared_task
from app.database.database import SessionLocal
from app.models import Product
from datetime import datetime, timedelta
import math

# Price adjustment thresholds
LOW_STOCK_THRESHOLD = 10  # Threshold for low stock
EXPIRATION_THRESHOLD_DAYS = 7  # Days before expiration to apply price reduction

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def update_product_prices(self):
    db = SessionLocal()
    try:
        # Get products with low stock or close to expiration
        products_to_update = db.query(Product).filter(
            (Product.stock <= LOW_STOCK_THRESHOLD) |
            (Product.expiry_date <= datetime.now() + timedelta(days=EXPIRATION_THRESHOLD_DAYS))
        ).all()

        for product in products_to_update:
            # Update price based on stock or expiration
            if product.stock <= LOW_STOCK_THRESHOLD:
                product.price = product.price * 1.2  # Increase price by 20% for low stock
            elif product.expiry_date <= datetime.now() + timedelta(days=EXPIRATION_THRESHOLD_DAYS):
                product.price = product.price * 0.8  # Decrease price by 20% for products close to expiration

            db.commit()
    except Exception as e:
        db.rollback()
        raise self.retry(exc=e)  # Retry in case of failure
    finally:
        db.close()
