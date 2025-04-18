from datetime import datetime
from app.celery_worker import celery
from app.database.session import async_session_maker
from sqlalchemy.future import select
from app.database.models import InventoryEntry
from sqlalchemy.ext.asyncio import AsyncSession

@celery.task
def adjust_expiring_prices():
    import asyncio
    asyncio.run(_adjust_prices())

async def _adjust_prices():
    async with async_session_maker() as session:
        result = await session.execute(select(InventoryEntry))
        inventory = result.scalars().all()

        now = datetime.utcnow()
        for item in inventory:
            days_to_expire = (item.expiration_date - now).days

            # Determine discount
            if days_to_expire <= 1:
                discount = 0.5
            elif days_to_expire <= 3:
                discount = 0.25
            elif days_to_expire <= 7:
                discount = 0.10
            else:
                discount = 0

            new_price = round(item.base_price * (1 - discount), 2)
            if item.current_price != new_price:
                item.current_price = new_price
                session.add(item)

        await session.commit()
