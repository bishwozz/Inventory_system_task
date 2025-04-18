import aioredis
from fastapi import Depends, HTTPException, Request
from starlette.status import HTTP_429_TOO_MANY_REQUESTS
import hashlib
from app.core.config import settings

redis = aioredis.from_url(settings.redis_url, decode_responses=True)

def get_key(ip: str, scope: str) -> str:
    return f"rate-limit:{hashlib.md5(f'{ip}:{scope}'.encode()).hexdigest()}"

async def rate_limiter(
    request: Request,
    scope: str = "global",
    limit: int = 10,
    period: int = 60
):
    ip = request.client.host
    key = get_key(ip, scope)

    current = await redis.get(key)
    if current and int(current) >= limit:
        raise HTTPException(
            status_code=HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded for {scope} ({limit} req/{period}s)"
        )

    pipeline = redis.pipeline()
    pipeline.incr(key)
    pipeline.expire(key, period)
    await pipeline.execute()
