from celery import Celery
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.product import Product
from app.utils.email import send_email_notification  # Assuming you have an email utility
from app.cache.redis_cache import get_from_cache, set_to_cache

# Initialize Celery
celery_app = Celery("inventory_system", broker="redis://localhost:6379/0")

@celery_app.task
def check_low_stock_alerts():
    """
    This task checks for products with low stock and sends alerts.
    """
    threshold = 10  # Define the low stock threshold
    cache_key = "low_stock_products"  # Cache key to store result
    
    # Try to fetch from cache first
    cached_result = get_from_cache(cache_key)
    if cached_result:
        low_stock_products = cached_result
    else:
        try:
            # Query for low-stock products if not cached
            with SessionLocal() as db:  # Use context management to ensure session is closed
                low_stock_products = db.query(Product).filter(Product.stock < threshold).all()
                
                # Store the result in cache for future use
                set_to_cache(cache_key, low_stock_products)
        except Exception as e:
            print(f"Error occurred while querying database: {e}")
            return {"message": "Error occurred while checking stock."}

    if low_stock_products:
        # Send an email or notification for each low-stock product
        for product in low_stock_products:
            try:
                send_email_notification(
                    subject="Low Stock Alert",
                    body=f"Product {product.name} has low stock ({product.stock} left).",
                    recipient="admin@domain.com"
                )
            except Exception as e:
                print(f"Error occurred while sending email for product {product.name}: {e}")
    
    return {"message": f"Low stock alerts checked for {len(low_stock_products)} products."}

celery_app = Celery("inventory_system", broker="redis://localhost:6379/0")

@celery_app.task
def trigger_low_stock_alert():
    """
    This task checks for products with low stock and sends alerts.
    """
    db = SessionLocal()  # Use your session creation method
    threshold = 10  # Define the low stock threshold
    
    # Query for low-stock products
    low_stock_products = db.query(Product).filter(Product.stock < threshold).all()
    
    if low_stock_products:
        # Send an email or notification (you can implement the `send_email_notification`)
        for product in low_stock_products:
            send_email_notification(
                subject="Low Stock Alert",
                body=f"Product {product.name} has low stock ({product.stock} left).",
                recipient="admin@domain.com"
            )

    db.close()