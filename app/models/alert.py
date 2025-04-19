from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.base import Base
from sqlalchemy.orm import relationship

class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, index=True)
    alert_type = Column(String, index=True) 
    threshold_days = Column(Integer, nullable=True)
    threshold_stock = Column(Integer, nullable=True) 
    message = Column(String)

    product_id = Column(Integer, ForeignKey("products.id"), index=True)
    product = relationship("Product", back_populates="alerts")
