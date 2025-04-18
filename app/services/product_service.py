import json
import redis
from fastapi import HTTPException, Depends
from app.models.product import Product
from app.database.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
from typing import Optional

# Connect to Redis
redis_client = redis.StrictRedis(host="redis", port=6379, db=0, decode_responses=True)

async def get_product_by_id(product_id: int, db: AsyncSession = Depends(get_db)) -> Product:
    # Check Redis cache first
    cached_product = redis_client.get(f"product:{product_id}")
    
    if cached_product:
        return json.loads(cached_product)  # Return cached product as a dict
    
    # If not found in cache, query the database
    result = await db.execute(select(Product).filter(Product.id == product_id))
    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    # Cache the product in Redis (with expiration time)
    redis_client.setex(f"product:{product_id}", 3600, json.dumps(product.to_dict()))  # Cache for 1 hour

    return product
