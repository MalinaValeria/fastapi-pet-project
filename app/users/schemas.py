from pydantic import BaseModel, EmailStr, Field


class SUserRegister(BaseModel):
    email: EmailStr = Field(..., description='Email address')
    password: str = Field(..., min_length=8, max_length=50, description='Password')
    password_confirm: str = Field(..., min_length=8, max_length=50, description='Confirm Password')
    username: str = Field(..., min_length=2, max_length=50, description='Username')


class SUserRead(BaseModel):
    id: int = Field(..., description='User ID')
    username: str = Field(..., description='Username')
