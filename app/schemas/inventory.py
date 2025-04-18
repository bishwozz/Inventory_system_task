from pydantic import BaseModel
from datetime import datetime


class InventoryAdd(BaseModel):
    product_id: int
    quantity: int
    expiration_date: datetime


class InventoryOut(BaseModel):
    id: int
    product_id: int
    quantity: int
    expiration_date: datetime
    added_at: datetime

    class Config:
        orm_mode = True
