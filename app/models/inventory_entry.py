from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base


class InventoryEntry(Base):
    __tablename__ = "inventory_entries"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    expiration_date = Column(DateTime)
    current_price = Column(Float)

    product = relationship("Product", back_populates="inventory_entries")