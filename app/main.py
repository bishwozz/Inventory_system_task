from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import health  # route
from app.core.config import settings
from app.api.v1.endpoints import auth
from app.api.v1.endpoints import products, inventory


app = FastAPI(
    title="Inventory System",
    version="1.0.0"
)

# Enable CORS (if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # can be restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include versioned API routes
app.include_router(health.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to Inventory System!"}

# Auth Routes
app.include_router(auth.router, prefix="/api/v1")

# Routes
app.include_router(products.router, prefix="/api/v1")
app.include_router(inventory.router, prefix="/api/v1")