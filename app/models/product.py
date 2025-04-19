# app/models/product.py
from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from app.db.base import Base
from sqlalchemy.orm import relationship

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    stock = Column(Integer)
    expiration_date = Column(DateTime)
    
    alerts = relationship("Alert", back_populates="product", cascade="all, delete-orphan")
    inventory_entries = relationship("InventoryEntry", back_populates="product", cascade="all, delete-orphan")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime)
