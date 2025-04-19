from sqlalchemy import Column, Integer, String, Float
from app.db.base import Base

class PricingRule(Base):
    __tablename__ = "pricing_rules"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, index=True)
    rule_type = Column(String, index=True)
    value = Column(Float)
    threshold_days = Column(Integer, nullable=True)
    threshold_stock = Column(Integer, nullable=True)
