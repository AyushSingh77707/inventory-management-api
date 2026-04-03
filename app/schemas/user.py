from pydantic import BaseModel,EmailStr,Field
from typing import Optional,Annotated
from app.models.user import RoleEnum
from datetime import datetime

#registration
class UserRegister(BaseModel):
    name:Annotated[str,Field(min_length=3,title="Enter User name which is registering")]
    email:Annotated[EmailStr,Field(title="Enter user email")]
    password:Annotated[str,Field(min_length=6,title="Enter password here",description="password must be of length 6 or above")]
    role:Optional[RoleEnum]=RoleEnum.customer

#login
class UserLogin(BaseModel):
    email:EmailStr
    password:str

#response ke liye
class UserResponse(BaseModel):
    id:int
    name:str
    email:str
    role:str
    is_active:bool
    created_at:datetime

    class Config:        #sqlalchemy object ko normal dictionary me convert krdega
        from_attributes=True
    
