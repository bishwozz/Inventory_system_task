from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.product import Product

def apply_price_adjustment_logic(product: Product) -> Product:
    if not product.expiration_date or not product.price:
        return product

    now = datetime.utcnow()
    days_to_expiry = (product.expiration_date - now).days

    if days_to_expiry <= 0:
        product.price = 0.0
    elif days_to_expiry <= 3:
        product.price *= 0.5
    elif days_to_expiry <= 7:
        product.price *= 0.75

    return product
