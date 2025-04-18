from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from typing import List
from app.database.session import get_db
from app.models.product import Product
from app.core.redis import redis_client
from pydantic import BaseModel
import json

router = APIRouter(prefix="/products", tags=["Products"])

# 📦 Pydantic Schemas
class ProductCreate(BaseModel):
    name: str
    description: str
    base_price: float

class ProductOut(ProductCreate):
    id: int

    class Config:
        orm_mode = True


# 🧾 Get all products
@router.get("/", response_model=List[ProductOut])
async def get_all_products(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product).order_by(Product.id))
    return result.scalars().all()


# 🧾 Get product by ID with Redis caching
@router.get("/{product_id}", response_model=ProductOut)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    key = f"product:{product_id}"

    cached = await redis_client.get(key)
    if cached:
        return json.loads(cached)

    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product_data = ProductOut.from_orm(product).dict()

    await redis_client.setex(key, 300, json.dumps(product_data))  # cache for 5 min

    return product_data


# ➕ Create a new product
@router.post("/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
async def create_product(product_in: ProductCreate, db: AsyncSession = Depends(get_db)):
    product = Product(**product_in.dict())
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product


# ✏️ Update a product and invalidate Redis
@router.put("/{product_id}", response_model=ProductOut)
async def update_product(
    product_id: int, product_in: ProductCreate, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    for field, value in product_in.dict().items():
        setattr(product, field, value)

    await db.commit()
    await db.refresh(product)

    await redis_client.delete(f"product:{product_id}")  # invalidate cache

    return product


# ❌ Delete a product and invalidate Redis
@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    await db.delete(product)
    await db.commit()

    await redis_client.delete(f"product:{product_id}")  # invalidate cache

    return None
