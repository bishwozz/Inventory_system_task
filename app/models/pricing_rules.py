from sqlalchemy import Column, Integer, Float, Interval
from .base import Base

class PricingRule(Base):
    __tablename__ = 'pricing_rules'

    id = Column(Integer, primary_key=True)
    days_before_expiration = Column(Integer, nullable=False)
    discount_percentage = Column(Float, nullable=False)
