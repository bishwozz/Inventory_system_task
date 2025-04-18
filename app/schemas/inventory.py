# app/schemas/inventory.py
from pydantic import BaseModel
from datetime import date

class InventoryCreate(BaseModel):
    product_id: int
    quantity: int
    expiration_date: date

class InventoryOut(BaseModel):
    id: int
    product_id: int
    quantity: int
    expiration_date: date
    adjusted_price: float

    class Config:
        orm_mode = True
