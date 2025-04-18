# app/schemas/alert.py
from pydantic import BaseModel
from datetime import datetime

class AlertBase(BaseModel):
    product_id: int
    message: str

class AlertCreate(AlertBase):
    pass

class AlertOut(AlertBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
