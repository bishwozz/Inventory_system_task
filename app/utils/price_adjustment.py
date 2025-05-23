from datetime import timedelta, date
from app.models.product import Product

def apply_price_adjustment(product: Product) -> Product:
    today = date.today()
    days_to_expiry = (product.expiration_date - today).days
    
    if days_to_expiry <= 7:  # Expiring within 7 days, apply a discount
        product.price *= 0.80  # 20% off
    elif days_to_expiry <= 30: 
        product.price *= 0.90 
    elif days_to_expiry < 0:  
        product.price *= 0.50
    
    return product
