from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_
from app.database.session import get_db
from app.models import InventoryEntry
from app.controller.inventory import InventoryCreate, InventoryOut
from typing import List
from datetime import datetime, timedelta

router = APIRouter(prefix="/inventory", tags=["Inventory"])

@router.post("/", response_model=InventoryOut)
async def add_inventory(entry: InventoryCreate, db: AsyncSession = Depends(get_db)):
    new_entry = InventoryEntry(**entry.dict())
    db.add(new_entry)
    await db.commit()
    await db.refresh(new_entry)
    return new_entry

@router.get("/", response_model=List[InventoryOut])
async def list_inventory(
    product_id: int = Query(None),
    expiring_in: int = Query(None),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(InventoryEntry)
    if product_id:
        stmt = stmt.where(InventoryEntry.product_id == product_id)
    if expiring_in:
        now = datetime.utcnow()
        stmt = stmt.where(InventoryEntry.expiration_date <= now + timedelta(days=expiring_in))

    result = await db.execute(stmt)
    return result.scalars().all()
