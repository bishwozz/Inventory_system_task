from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from app.db.database import SessionLocal, get_product_from_cache, set_product_to_cache, get_db
from app.models.product import Product
from app.schemas.product import ProductOut, ProductCreate, ProductUpdate, ProductListResponse, PaginationMeta
from app.services.auth import get_current_user, require_role
from app.utils.price_adjustment import apply_price_adjustment
from app.utils.response import success_response, error_response
from app.models.user import User

router = APIRouter()


# List Products (Filter by expiration range, pagination)
@router.get("/list", response_model=ProductListResponse)
def list_products(
    expiring_in: Optional[int] = Query(None, description="Filter products expiring in N days"),
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    skip = (page - 1) * limit

    query = db.query(Product)

    if expiring_in:
        threshold = datetime.utcnow() + timedelta(days=expiring_in)
        query = query.filter(Product.expiration_date <= threshold)

    total_products = query.count()
    products = query.offset(skip).limit(limit).all()
    total_pages = (total_products + limit - 1) // limit

    return ProductListResponse(
        status="success",
        message="Product list fetched successfully",
        data=[ProductOut.from_orm(product) for product in products],
        pagination=PaginationMeta(
            page=page,
            limit=limit,
            total_pages=total_pages,
            total_products=total_products,
        )
    )
# Create Product (Admin only)
@router.post("/", response_model=None, dependencies=[Depends(require_role("admin"))])
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    set_product_to_cache(db_product)  # optional: cache on create
    return success_response(data=db_product, message="Product created successfully")


# Get Single Product (with cache)
@router.get("/{product_id}", response_model=None)
def get_product(product_id: int, db: Session = Depends(get_db)):
    db_product = get_product_from_cache(product_id)
    if not db_product:
        db_product = db.query(Product).filter(Product.id == product_id).first()
        if not db_product:
            return error_response("Product not found", 404)
        set_product_to_cache(db_product)
    return success_response(data=db_product)


# Update Product (Admin only)
@router.put("/{product_id}", response_model=None, dependencies=[Depends(require_role("admin"))])
def update_product(product_id: int, updated: ProductUpdate, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        return error_response("Product not found", 404)

    for key, value in updated.dict(exclude_unset=True).items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)
    set_product_to_cache(db_product)
    return success_response(data=db_product, message="Product updated successfully")


# Delete Product (Admin only)
@router.delete("/{product_id}", response_model=None, dependencies=[Depends(require_role("admin"))])
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        return error_response("Product not found", 404)

    db.delete(db_product)
    db.commit()
    return success_response(message="Product deleted successfully")


# Apply price adjustment (endpoint to trigger price change)
@router.post("/{product_id}/adjust-price")
def adjust_product_price(
    product_id: int, db: Session = Depends(get_db)
    ):
    product = db.query(Product).filter(Product.id == product_id).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Apply the price adjustment
    product = apply_price_adjustment(product)
    
    db.commit()
    db.refresh(product)
    set_product_to_cache(product)  # Update the cache after adjustment
    
    return {"message": "Price adjusted", "product": product}