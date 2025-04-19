import redis
import json
from app.models.product import Product

# Connect to Redis (make sure Redis is running and matches Docker setup)
redis_client = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)

def set_to_cache(key: str, data, ttl: int = 300):
    redis_client.setex(key, ttl, json.dumps(data, default=str))

def get_from_cache(key: str):
    value = redis_client.get(key)
    return json.loads(value) if value else None

def set_product_to_cache(product: Product):
    key = f"product:{product.id}"
    data = {
        "id": product.id,
        "name": product.name,
        "stock": product.stock,
        "expiration_date": str(product.expiration_date),
        "price": product.price
    }
    redis_client.set(key, json.dumps(data), ex=3600)  # Cache for 1 hour

def get_product_from_cache(product_id: int):
    key = f"product:{product_id}"
    data = redis_client.get(key)
    if data:
        return json.loads(data)
    return None