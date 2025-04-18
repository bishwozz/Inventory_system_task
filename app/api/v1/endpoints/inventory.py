# app/api/v1/endpoints/inventory.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import date, timedelta
from app.models.base import get_db
from app.models.inventory_entry import InventoryEntry
from app.schemas.inventory import InventoryCreate, InventoryOut

router = APIRouter()

@router.post("/", response_model=InventoryOut)
async def add_inventory(entry: InventoryCreate, db: AsyncSession = Depends(get_db)):
    adjusted_price = calculate_adjusted_price(entry.expiration_date)
    new_entry = InventoryEntry(**entry.dict(), adjusted_price=adjusted_price)
    db.add(new_entry)
    await db.commit()
    await db.refresh(new_entry)
    return new_entry

@router.get("/", response_model=list[InventoryOut])
async def get_inventory(expiring_in: int = Query(None), db: AsyncSession = Depends(get_db)):
    query = select(InventoryEntry)
    if expiring_in:
        cutoff = date.today() + timedelta(days=expiring_in)
        query = query.where(InventoryEntry.expiration_date <= cutoff)
    result = await db.execute(query)
    return result.scalars().all()

def calculate_adjusted_price(expiration_date: date):
    days_left = (expiration_date - date.today()).days
    if days_left < 3:
        return 0.5  # 50% discount
    elif days_left < 7:
        return 0.8  # 20% discount
    return 1.0  # no discount (multiplier)
