from app.worker import celery_app
from app.database.session import async_session
from sqlalchemy.future import select
from sqlalchemy import func
from datetime import datetime, timedelta

from app.models import InventoryEntry, Product
import logging

logger = logging.getLogger(__name__)

@celery_app.task
def scan_inventory_and_adjust():
    logger.info("🔄 Running periodic inventory scan...")

    async def _run():
        async with async_session() as session:
            now = datetime.utcnow()
            near_expiry = now + timedelta(days=3)

            # 1. Adjust prices for near-expiry items
            result = await session.execute(
                select(Product).join(InventoryEntry).where(InventoryEntry.expiration_date <= near_expiry)
            )
            products = result.scalars().all()
            for product in products:
                if product.price > 0:
                    old_price = product.price
                    product.price *= 0.8  # Apply 20% discount
                    logger.info(f"💸 Price adjusted for {product.name}: {old_price} → {product.price}")

            # 2. Low stock alerts
            low_stock_result = await session.execute(
                select(InventoryEntry.product_id, func.sum(InventoryEntry.quantity).label("total"))
                .group_by(InventoryEntry.product_id)
                .having(func.sum(InventoryEntry.quantity) < 5)
            )
            alerts = low_stock_result.all()
            for product_id, total_qty in alerts:
                logger.warning(f"⚠️ Low stock alert - Product ID {product_id} has {total_qty} items left!")

            await session.commit()

    import asyncio
    asyncio.run(_run())
