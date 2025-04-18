# app/models/product.py
from sqlalchemy import Column, Integer, String, Float, DateTime
from app.models.base import Base
from sqlalchemy.orm import relationship
from datetime import datetime


class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, default=0)
    expiration_date = Column(DateTime, nullable=True)
    alerts = relationship("Alert", back_populates="product", cascade="all, delete-orphan")

    created_at = Column(DateTime, default=datetime.utcnow)

