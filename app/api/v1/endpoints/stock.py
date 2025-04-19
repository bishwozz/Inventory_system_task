from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.database import SessionLocal, get_db
from app.models.product import Product
from app.services.auth import get_current_user
from app.utils.rate_limiter import is_rate_limited
from app.utils.alert import send_low_stock_alert
from app.cache.redis_cache import set_product_to_cache, get_product_from_cache
from app.models.user import User
from app.models.alert import Alert
from datetime import datetime, timedelta
from typing import List, Optional

router = APIRouter()

# Add Stock
@router.put("/products/{product_id}/add_stock/")
def add_stock(product_id: int, stock: int, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    # Check rate-limiting
    is_rate_limited(current_user.id) 
    
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    db_product.stock += stock
    db.commit()
    db.refresh(db_product)

    # Check if stock is below threshold for alert
    if db_product.stock <= 10:
        alert = Alert(
            product_id=db_product.id,
            alert_type="Low Stock",
            message=f"Product '{db_product.name}' has low stock ({db_product.stock})",
            created_at=datetime.utcnow(),
        )
        db.add(alert)
        db.commit()

    return {"message": "Stock added successfully", "stock": db_product.stock}

# Remove Stock
@router.put("/products/{product_id}/remove_stock/")
def remove_stock(product_id: int, stock: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Check rate-limiting
    is_rate_limited(current_user.id) 
    
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    if db_product.stock < stock:
        raise HTTPException(status_code=400, detail="Not enough stock to remove")

    db_product.stock -= stock
    db.commit()
    db.refresh(db_product)

    # Check if stock is below threshold for alert
    if db_product.stock <= 10:
        alert = Alert(
            product_id=db_product.id,
            alert_type="Low Stock",
            message=f"Product '{db_product.name}' has low stock ({db_product.stock})",
            created_at=datetime.utcnow(),
        )
        db.add(alert)
        db.commit()

    return {"message": "Stock removed successfully", "stock": db_product.stock}