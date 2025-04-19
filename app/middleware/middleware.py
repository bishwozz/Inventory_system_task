from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.db.database import get_product_from_cache, set_product_to_cache
from app.utils.response import error_response
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.auth import get_current_user

class CacheMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Check cache if the request is for product and includes product_id
        if "product_id" in request.path_params:
            product_id = request.path_params["product_id"]
            db = get_db()
            db_product = get_product_from_cache(product_id)
            
            if not db_product:
                response = await call_next(request)
                db_product = response.body
                set_product_to_cache(db_product)
                return response
            return Response(content=db_product, status_code=200)
        response = await call_next(request)
        return response
    
# class RoleCheckMiddleware(BaseHTTPMiddleware):
#     async def dispatch(self, request: Request, call_next):
#         # Check if the user is authorized based on role
#         user = await get_current_user(request) 
#         required_role = request.state.required_role  
        
#         if required_role and user.role != required_role:
#            return error_response(f"Insufficient permissions. Required: {required_role}", 403)
        
#         response = await call_next(request)
#         return response
