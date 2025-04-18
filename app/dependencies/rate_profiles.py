from fastapi import Depends
from app.dependencies.rate_limit import rate_limiter

def global_limiter():
    return rate_limiter(scope="global", limit=60, period=60)

def login_limiter():
    return rate_limiter(scope="login", limit=10, period=60)

