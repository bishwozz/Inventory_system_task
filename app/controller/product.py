from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from app.db.database import get_db
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductOut, ProductUpdate
from app.models.pricing_rule import PricingRule
from app.services.auth import require_role, get_current_user
from app.utils.response import success_response, error_response
from app.models.user import User

router = APIRouter()

# Create Product (Admin only)
@router.post("/", response_model=None, dependencies=[Depends(require_role("admin"))])
def create_product(product: ProductCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    
    # Create a pricing rule for the product
    pricing_rule = PricingRule(
        product_id=db_product.id,
        price_change_percentage=10,
        applies_before_expiration=datetime.utcnow() + timedelta(days=15)
    )
    db.add(pricing_rule)
    db.commit()

    return success_response(data=db_product, message="Product created successfully")


# Get Single Product (with cache)
@router.get("/{product_id}", response_model=None)
def get_product(product_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        return error_response("Product not found", 404)
    return success_response(data=db_product)


# Update Product (Admin only)
@router.put("/{product_id}", response_model=None, dependencies=[Depends(require_role("admin"))])
def update_product(product_id: int, updated: ProductUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        return error_response("Product not found", 404)

    for key, value in updated.dict(exclude_unset=True).items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)
    return success_response(data=db_product, message="Product updated successfully")


# Delete Product (Admin only)
@router.delete("/{product_id}", response_model=None, dependencies=[Depends(require_role("admin"))])
def delete_product(product_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        return error_response("Product not found", 404)

    db.delete(db_product)
    db.commit()
    return success_response(message="Product deleted successfully")


# List Products (Filter by expiration range, pagination)
@router.get("/", response_model=List[ProductOut])
def list_products(
    expiring_in: Optional[int] = Query(None, description="Filter products expiring in N days"),
    page: int = Query(1, ge=1, description="Page number (starts from 1)"),
    limit: int = Query(10, le=100, description="Number of products per page (max 100)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) 
):
    # Calculate offset for pagination
    skip = (page - 1) * limit

    query = db.query(Product)
    if expiring_in:
        threshold = datetime.utcnow() + timedelta(days=expiring_in)
        query = query.filter(Product.expiration_date <= threshold)

    total_products = query.count()

    products = query.offset(skip).limit(limit).all()

    # Calculate the total number of pages
    total_pages = (total_products + limit - 1) // limit 

    return success_response(
        data=products,
        message="Product list fetched",
        pagination={
            "page": page,
            "limit": limit,
            "total_pages": total_pages,
            "total_products": total_products
        }
    )