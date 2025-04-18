from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.db.database import get_db, SessionLocal
from app.models.product import Product

router = APIRouter()

@router.get("/inventory/")
def get_inventory_by_expiration(
    expiring_in: int = Query(7, description="Number of days until expiration"),
    db: Session = Depends(get_db)
):
    cutoff_date = datetime.utcnow() + timedelta(days=expiring_in)
    products = db.query(Product).filter(Product.expiration_date <= cutoff_date).all()
    return {
        "expiring_within_days": expiring_in,
        "products": [
            {
                "id": p.id,
                "name": p.name,
                "stock": p.stock,
                "expiration_date": p.expiration_date,
                "price": p.price
            } for p in products
        ]
    }

# @router.get("/inventory/")
# def get_inventory(expiring_in: int = None):
#     db = SessionLocal()
#     query = db.query(Product)
    
#     if expiring_in:
#         expiration_date = datetime.utcnow() + timedelta(days=expiring_in)
#         query = query.filter(Product.expiration_date <= expiration_date)
    
#     products = query.all()
#     return products
