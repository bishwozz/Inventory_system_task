import redis
from fastapi import HTTPException, Depends
from app.models.product import Product
from app.database.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime, timedelta

# Connect to Redis
redis_client = redis.StrictRedis(host="redis", port=6379, db=0, decode_responses=True)

async def adjust_stock(product_id: int, quantity: int, db: AsyncSession = Depends(get_db)):
    # Rate-limit logic using Redis: Check if adjustment has been made in the last 10 seconds
    rate_limit_key = f"rate_limit:stock_adjust:{product_id}"
    last_adjusted = redis_client.get(rate_limit_key)

    if last_adjusted:
        raise HTTPException(status_code=429, detail="Too many stock adjustments, try again later.")
    
    # Update stock in the database
    result = await db.execute(select(Product).filter(Product.id == product_id))
    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Adjust stock
    product.stock += quantity  # Assuming stock is a column in Product model
    db.add(product)
    await db.commit()

    # Store the rate-limit timestamp in Redis (expires after 10 seconds)
    redis_client.setex(rate_limit_key, 10, "true")

    return {"message": "Stock adjusted successfully", "product_id": product_id, "new_stock": product.stock}
