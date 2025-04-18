from fastapi import FastAPI
from app.api.v1 import api_v1
from app.middleware.middleware import CacheMiddleware

app = FastAPI(title="Inventory System API", version="1.0", debug="TRUE")

# Add the middleware to your app
app.add_middleware(CacheMiddleware)
app.include_router(api_v1.api_router, prefix="/api/v1")


@app.get("/test")
def read_root():
    return {"message": "Welcome to the inventory system API"}
