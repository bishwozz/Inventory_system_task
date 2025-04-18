# app/utils/rate_limiter.py

import time
import redis
from fastapi import HTTPException

r = redis.Redis(host="redis", port=6379, decode_responses=True)

def is_rate_limited(user_id: int, limit: int = 5, period: int = 60):
    """
    Rate limit stock adjustment per user_id.
    Default: 5 actions per 60 seconds.
    """
    key = f"stock-adjust:{user_id}"
    current_count = r.get(key)

    if current_count and int(current_count) >= limit:
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Try again later.")

    # Increment the count and set expiry if it's new
    pipe = r.pipeline()
    pipe.incr(key, 1)
    pipe.expire(key, period)
    pipe.execute()
