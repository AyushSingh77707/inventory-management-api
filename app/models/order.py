from sqlalchemy import Column,String,Integer,DateTime,ForeignKey,Float,func
from app.database import Base
from sqlalchemy.orm import relationship


class Order(Base):
    __tablename__="orders"

    id=Column(Integer,primary_key=True,index=True)
    user_id=Column(Integer,ForeignKey("users.id"),nullable=False)
    status=Column(String,default="Pending")
    total_amount=Column(Float,default=0.0)
    created_at=Column(DateTime(timezone=True),server_default=func.now())

    user=relationship("User",back_populates="orders")
    items=relationship("OrderItem",back_populates="order")

class OrderItem(Base):
    __tablename__="order_items"
    id=Column(Integer,primary_key=True,index=True)
    order_id=Column(Integer,ForeignKey("orders.id"),nullable=False)
    product_id=Column(Integer,ForeignKey("products.id"),nullable=False)
    quantity=Column(Integer,nullable=False)
    price=Column(Float,nullable=False,default=0.00)

    order=relationship("Order",back_populates="items")
    product=relationship("Product")


