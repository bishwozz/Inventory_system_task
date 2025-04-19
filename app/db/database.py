import redis
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from app.db.base import Base

# Database URL from environment variable or default
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:inventory_pass@db:5432/inventory_db")

# SQLAlchemy engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Redis connect
cache = redis.Redis(host="localhost", port=6379, db=0)


def get_product_from_cache(product_id: int):
    product_data = cache.get(f"product:{product_id}")
    if product_data:
        return json.loads(product_data)
    return None


def set_product_to_cache(product):
    cache.set(f"product:{product.id}", json.dumps(product.__dict__))


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create all tables
Base.metadata.create_all(bind=engine)
