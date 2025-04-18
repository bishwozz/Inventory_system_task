# app/models/inventory.py
from sqlalchemy import Column, Integer, ForeignKey, Date, Float
from sqlalchemy.orm import relationship
from app.models.base import Base

class InventoryEntry(Base):
    __tablename__ = "inventory_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    expiration_date = Column(Date)
    adjusted_price = Column(Float)

    product = relationship("Product", backref="inventory_entries")
