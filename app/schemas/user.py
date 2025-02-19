from pydantic import BaseModel, EmailStr, constr

class UserBase(BaseModel):
    username: constr(min_length=3, max_length=50)
    email: EmailStr

class UserCreate(UserBase):
    password: constr(min_length=8)

class UserResponse(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True 