from pydantic import BaseModel,EmailStr
from typing import Optional

#registration
class UserRegister(BaseModel):
    name:str
    email:EmailStr
    password:str
    role:Optional[str]="Staff"

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

    class Config:        #sqlalchemy object ko normal dictionary me convert krdega
        from_attributes=True
    
