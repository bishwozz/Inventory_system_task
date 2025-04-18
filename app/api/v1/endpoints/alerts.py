# app/api/v1/endpoints/alerts.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schemas.alert import AlertCreate, AlertOut
from app.models.alert import Alert
from app.models.product import Product
from app.database.session import get_db
from app.services import alerts

router = APIRouter()

# Get alerts
@router.get("/", response_model=List[AlertOut])
async def get_alerts(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Alert).order_by(Alert.created_at.desc()))
    alerts = result.scalars().all()
    return alerts

# Create an alert
@router.post("/", response_model=AlertOut)
async def create_alert(alert: AlertCreate, db: AsyncSession = Depends(get_db)):
    # Check if the product exists
    result = await db.execute(select(Product).filter(Product.id == alert.product_id))
    product = result.scalars().first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Create and save the alert
    db_alert = Alert(product_id=alert.product_id, message=alert.message)
    db.add(db_alert)
    await db.commit()
    await db.refresh(db_alert)

    return db_alert


@router.get("/alerts/expiring", tags=["Alerts"])
async def expiring_soon(db: AsyncSession = Depends(get_db)):
    products = await alerts.get_expiring_soon_products(db)
    return {"expiring_soon": products}

@router.get("/alerts/low-stock", tags=["Alerts"])
async def low_stock(db: AsyncSession = Depends(get_db)):
    products = await alerts.get_low_stock_products(db)
    return {"low_stock": products}