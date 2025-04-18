from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.product import Product

EXPIRY_DAYS_THRESHOLD = 7
LOW_STOCK_THRESHOLD = 5

async def get_expiring_soon_products(db: AsyncSession):
    today = datetime.utcnow().date()
    limit_date = today + timedelta(days=EXPIRY_DAYS_THRESHOLD)

    result = await db.execute(
        select(Product).where(Product.expiration_date <= limit_date)
    )
    return result.scalars().all()

async def get_low_stock_products(db: AsyncSession):
    result = await db.execute(
        select(Product).where(Product.quantity < LOW_STOCK_THRESHOLD)
    )
    return result.scalars().all()
