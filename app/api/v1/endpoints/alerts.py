from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database.session import get_db
from app.models.alert import Alert
from typing import List
from pydantic import BaseModel

router = APIRouter(prefix="/alerts", tags=["Alerts"])

class AlertOut(BaseModel):
    id: int
    product_id: int
    message: str
    created_at: str

    class Config:
        orm_mode = True

@router.get("/", response_model=List[AlertOut])
async def get_alerts(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Alert).order_by(Alert.created_at.desc()))
    return result.scalars().all()
