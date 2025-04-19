import redis
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from app.db.base import Base
from app.schemas.product import ProductBase

# Database URL from environment variable or default
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:inventory_pass@db:5432/inventory_db")

# SQLAlchemy engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Redis connect
cache = redis.Redis(host="redis", port=6379, db=0)


def get_product_from_cache(product_id: int):
    product_data = cache.get(f"product:{product_id}")
    if product_data:
        return json.loads(product_data)
    return None


def set_product_to_cache(product):
    product_data = {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": str(product.price),
        "expiration_date": product.expiration_date.isoformat() if product.expiration_date else None,
        "created_at": product.created_at.isoformat() if product.created_at else None,
    }
    cache.set(f"product:{product.id}", json.dumps(product_data))


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create all tables
Base.metadata.create_all(bind=engine)
