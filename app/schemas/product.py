from pydantic import BaseModel
from datetime import date
from typing import Optional, List
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    expiration_date: datetime
    stock: int

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True


class ProductIn(BaseModel):
    name: str
    description: Optional[str] = None
    expiration_date: datetime
    stock: int
    price: float


class ProductOut(ProductBase):
    id: int
    name: str
    description: Optional[str] = None
    expiration_date: datetime
    stock: int
    price: float

    model_config = {
        "from_attributes": True
    }

class PaginationMeta(BaseModel):
    page: int
    limit: int
    total_pages: int
    total_products: int
class ProductListResponse(BaseModel):
    status: str
    message: str
    data: List[ProductOut]
    pagination: PaginationMeta

