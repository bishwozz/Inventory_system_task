# app/models/inventory.py
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime

class InventoryEntry(Base):
    __tablename__ = "inventory_entries"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), index=True)
    quantity = Column(Integer, nullable=False)
    expiration_date = Column(DateTime, nullable=False)
    added_at = Column(DateTime, default=datetime.utcnow)

    # Use string-based reference for the relationship
    product = relationship("Product", back_populates="inventory_entries")
