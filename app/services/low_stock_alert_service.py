from app.cache.redis_cache import get_from_cache, set_to_cache
from app.db.database import SessionLocal
from app.models.product import Product
from app.utils.email import send_email_notification

def check_low_stock_alerts():
    """
    This function checks for low stock products using caching first.
    If not found in cache, it queries the database.
    """
    cache_key = "low_stock_products"
    
    low_stock_products = get_from_cache(cache_key)
    if not low_stock_products:
        db = SessionLocal()
        low_stock_products = db.query(Product).filter(Product.stock < 10).all()
        set_to_cache(cache_key, low_stock_products)
        db.close()
    
    # Send alerts if any low-stock products exist
    if low_stock_products:
        for product in low_stock_products:
            send_email_notification(
                subject="Low Stock Alert",
                body=f"Product {product.name} has low stock ({product.stock} left).",
                recipient="admin@domain.com"
            )
