from app.database import Base
from sqlalchemy import String,Integer,DateTime,Column,Float,Boolean,Numeric
from sqlalchemy import func

from enum import Enum
class CategoryEnum(str,Enum):
    electronics="electronics"
    clothing="clothing"
    food="food"



class Product(Base):
    __tablename__="products"

    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,nullable=False)
    category=CategoryEnum
    description=Column(String)
    price=Column(Numeric(precision=15,scale=2),nullable=False)
    stock_quantity=Column(Integer,default=0)
    created_at=Column(DateTime(timezone=True),server_default=func.now())
    
    #soft delete
    is_active=Column(Boolean,default=True)
    updated_at=Column(DateTime(timezone=True),onupdate=func.now())