from app.celery_worker import celery
from app.database.session import async_session_maker
from sqlalchemy.future import select
from sqlalchemy import func
from app.models.inventory_entry import InventoryEntry
from app.models.alert import Alert
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

LOW_STOCK_THRESHOLD = 10

@celery.task
def check_low_stock():
    import asyncio
    asyncio.run(_check_low_stock())

async def _check_low_stock():
    async with async_session_maker() as session:
        # Get total quantity grouped by product
        result = await session.execute(
            select(InventoryEntry.product_id, func.sum(InventoryEntry.quantity))
            .group_by(InventoryEntry.product_id)
        )
        stock_summary = result.all()

        for product_id, total_qty in stock_summary:
            if total_qty < LOW_STOCK_THRESHOLD:
                # Prevent duplicate alerts for same product on same day
                today = datetime.utcnow().date()
                existing = await session.execute(
                    select(Alert).where(
                        Alert.product_id == product_id,
                        func.date(Alert.created_at) == today
                    )
                )
                if not existing.scalar_one_or_none():
                    alert = Alert(
                        product_id=product_id,
                        message=f"Low stock: Only {total_qty} units left"
                    )
                    session.add(alert)

        await session.commit()
