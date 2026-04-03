from sqlalchemy import Column,String,Integer,Boolean,DateTime
from sqlalchemy.sql import func
from app.database import Base
from sqlalchemy.orm import relationship
from enum import Enum

class RoleEnum(str,Enum):
    admin="admin"
    customer="customer"
    manager="manager"
    staff="staff"

class User(Base):
    __tablename__="users"

    id=Column(Integer,primary_key=True,index=True)      #index=True => search fast
    name=Column(String,nullable=False)
    email=Column(String,unique=True,nullable=False)
    password=Column(String,nullable=False)
    role=Column(RoleEnum,default=RoleEnum.customer)
    is_active=Column(Boolean,default=True)
    created_at=Column(DateTime(timezone=True),server_default=func.now()) #server_default=func.now()=>automatic time save

    orders=relationship("Order",back_populates="user")