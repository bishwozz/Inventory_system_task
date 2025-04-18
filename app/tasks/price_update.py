# app/tasks.py
from celery import Celery
from app.db.database import SessionLocal
from app.models.product import Product
from app.utils.price_adjustment import apply_price_adjustment

celery_app = Celery('tasks', broker='redis://localhost:6379/0')

@celery_app.task
def adjust_prices_periodically():
    db = SessionLocal()
    products = db.query(Product).all()

    for product in products:
        product = apply_price_adjustment(product)
        db.commit()
        db.refresh(product)
    db.close()
