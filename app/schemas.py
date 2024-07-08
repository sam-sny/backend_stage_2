from pydantic import BaseModel, EmailStr
from typing import List, Optional
from uuid import UUID

class UserBase(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    phone: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserResponse(BaseModel):
    status: str
    message: str
    data: dict

    class Config:
        orm_mode = True
        from_attributes = True

class OrganisationBase(BaseModel):
    name: str
    description: str

class OrganisationCreate(OrganisationBase):
    pass

class OrganisationCreateRequest(BaseModel):
    name: str
    description: str = ""

class OrganisationResponse(BaseModel):
    status: str
    message: str
    data: dict

    class Config:
        orm_mode = True
        from_attributes = True

class AddUserRequest(BaseModel):
    userId: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str
    exp: int

class RegisterResponse(BaseModel):
    status: str
    message: str
    data: dict

    class Config:
        orm_mode = True
        from_attributes = True

class ErrorResponse(BaseModel):
    status: str
    message: str
    statusCode: int

class LoginResponse(BaseModel):
    status: str
    message: str
    data: dict

    class Config:
        orm_mode = True
        from_attributes = True