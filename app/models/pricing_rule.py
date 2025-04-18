from sqlalchemy import Column, Integer, String, Float
from app.db.base import Base

class PricingRule(Base):
    __tablename__ = "pricing_rules"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, index=True)
    rule_type = Column(String, index=True)  # e.g., "expiration", "stock"
    value = Column(Float)  # Discount or price adjustment value
    threshold_days = Column(Integer, nullable=True)  # For expiration rule
    threshold_stock = Column(Integer, nullable=True)  # For stock rule
