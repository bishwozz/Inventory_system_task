# app/main.py
from fastapi import FastAPI
from app.config.config import settings
from app.api.v1.endpoints import example 
from app.api.v1.api import api_router


app = FastAPI(
    title="Inventory System",
    version="1.0.0",
    debug=True
)
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Inventory System API is running"}
