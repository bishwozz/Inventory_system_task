from fastapi import APIRouter
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.product import Product

router = APIRouter()

@router.get("/alerts/low_stock/")
def low_stock_alert(threshold: int = 5):
    db = SessionLocal()
    low_stock_products = db.query(Product).filter(Product.stock <= threshold).all()
    if not low_stock_products:
        return {"message": "No low stock items"}
    
    return low_stock_products
