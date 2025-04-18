from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.product import Product
from app.services.price_adjustment_service import apply_price_adjustment_logic
from app.celery_worker import celery_app

@celery_app.task
def apply_dynamic_pricing():
    db: Session = SessionLocal()
    products = db.query(Product).all()

    for product in products:
        original_price = product.price
        updated_product = apply_price_adjustment_logic(product)
        if updated_product.price != original_price:
            db.add(updated_product)

    db.commit()
    db.close()


