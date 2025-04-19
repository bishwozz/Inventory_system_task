from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User
from app.utils.security import hash_password
from app.schemas.user import UserCreate
from app.utils.response import success_response, error_response
from app.schemas.user import UserLogin, LoginRequest
from app.utils.security import verify_password
from app.services.auth import create_access_token
from app.schemas.user import UserOut, UserResponse
import logging
from fastapi.responses import JSONResponse


router = APIRouter()
logger = logging.getLogger(__name__)

# Register User
@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = User.hash_password(user.password)
    new_user = User(username=user.username, email=user.email, password=hashed_password, role_id=2)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return success_response(data=UserResponse.from_orm(new_user).dict(), message="User registered successfully")

# Login User
@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user or not User.verify_password(request.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    # Generate token
    access_token = create_access_token(data={"sub": user.id})

    return success_response(
        data=UserResponse.from_orm(user).dict(),
        access_token=access_token,
        token_type="bearer",
        message="User registered successfully"
    )
