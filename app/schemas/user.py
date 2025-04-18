from pydantic import BaseModel
from app.models import User
from typing import List

class UserCreate(BaseModel):
    email: str
    username: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

    class Config:
        orm_mode = True
class LoginRequest(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    username: str
    email: str
    id: int

    class Config:
        orm_mode = True
        from_attributes = True 


# Convert User object to UserResponse schema
def user_to_response(user: User):
    return UserResponse.from_orm(user)


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    role_id: int

    class Config:
        orm_mode = True