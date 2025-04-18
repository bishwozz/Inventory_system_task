from fastapi import HTTPException, Depends
from app.models.user import User
from app.database.database import get_db
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from app.utils.security import get_current_user
from app.schemas.user import UserOut

# OAuth2PasswordBearer is the dependency used for security
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_user_role(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def role_required(required_role: str):
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role.name != required_role:
            raise HTTPException(
                status_code=403, detail="You do not have permission to access this resource"
            )
        return current_user
    return role_checker
