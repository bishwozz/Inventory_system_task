from celery import Celery
from sqlalchemy.orm import Session
from app.models.product import Product
from app.utils.config import LOW_STOCK_THRESHOLD
from app.database.database import get_db
from app.utils.notification import send_low_stock_alert 

celery_app = Celery("low_stock_alerts", broker="redis://localhost:6379/0")

@celery_app.task
def check_low_stock_products():
    db: Session = next(get_db())  # Assume get_db() provides a session generator

    # Get products with stock below the threshold
    low_stock_products = db.query(Product).filter(Product.quantity < LOW_STOCK_THRESHOLD).all()

    if low_stock_products:
        # Send an alert (mocked for now)
        for product in low_stock_products:
            send_low_stock_alert(product)

    return f"Checked low stock products, found {len(low_stock_products)} items with low stock."

