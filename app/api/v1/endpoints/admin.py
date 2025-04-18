from fastapi import APIRouter, Depends
from app.models.user import User
from app.services.rbac import role_required
from app.schemas.user import UserOut
from app.database import get_db
from sqlalchemy.orm import Session
from app.utils.security import get_current_user

router = APIRouter()

@router.get("/admin-dashboard", response_model=UserOut)
def get_admin_dashboard(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Only users with "Admin" role can access this
    return {"message": f"Welcome {current_user.email} to the Admin Dashboard"}
