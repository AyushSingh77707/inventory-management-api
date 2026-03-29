from app.database import Base
from sqlalchemy import String,Integer,DateTime,Column,Float
from sqlalchemy import func



class Product(Base):
    __tablename__="products"

    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,nullable=False)
    category=Column(String,nullable=False)
    description=Column(String)
    price=Column(Float,nullable=False)
    stock_quantity=Column(Integer,default=0)
    created_at=Column(DateTime(timezone=True),server_default=func.now())