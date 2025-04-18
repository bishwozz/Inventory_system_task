from fastapi import APIRouter, Depends
from app.api.v1.endpoints import auth, product, inventory
from app.services.auth import get_current_user

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(product.router, prefix="/products", tags=["Products"], dependencies=[Depends(get_current_user)])
api_router.include_router(inventory.router, prefix="/inventory", tags=["Inventory"])

