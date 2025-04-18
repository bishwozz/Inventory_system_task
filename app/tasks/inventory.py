from celery import Celery
from datetime import datetime, timedelta
from app.db.database import SessionLocal
from app.models.product import Product

celery_app = Celery("inventory_system", broker="redis://localhost:6379/0")

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
