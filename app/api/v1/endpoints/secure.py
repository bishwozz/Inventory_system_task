from fastapi import APIRouter, Depends, HTTPException
from app.services.auth import get_user_by_email
from app.database import SessionLocal
from app.schemas.auth import TokenData
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "secret_key_for_jwt_token" 
ALGORITHM = "HS256"

@router.get("/secure-data")
def get_secure_data(token: str = Depends(oauth2_scheme), db: SessionLocal = Depends()):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        token_data = TokenData(email=email)
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    
    user = get_user_by_email(db, email=email)
    return {"msg": "This is a secure endpoint", "user": user.username, "role": user.role.name}
