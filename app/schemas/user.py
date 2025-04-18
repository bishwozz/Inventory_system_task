# app/schemas/user.py
from pydantic import BaseModel, EmailStr
from typing import Optional

# Role schema
class RoleBase(BaseModel):
    name: str

class RoleOut(RoleBase):
    id: int

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role_id: Optional[int] = None  # Role is optional during registration

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    role_id: int
    is_active: bool

    class Config:
        orm_mode = True

# For login
class LoginForm(BaseModel):
    email: str
    password: str