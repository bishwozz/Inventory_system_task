from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.product import Product
from datetime import datetime, timedelta

router = APIRouter()

@router.put("/products/{product_id}/apply_price_adjustment/")
def apply_price_adjustment(product_id: int):
    db = SessionLocal()
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Apply a 10% discount for products expiring in the next 7 days
    if db_product.expiration_date <= datetime.utcnow() + timedelta(days=7):
        db_product.price = db_product.price * 0.9  # 10% discount
    
    db.commit()
    db.refresh(db_product)
    return {"message": "Price adjusted", "new_price": db_product.price}
