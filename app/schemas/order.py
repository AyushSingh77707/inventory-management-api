from pydantic import BaseModel
from typing import Optional,List

class OrderItemCreate(BaseModel):
    product_id:int
    quantity:int

class OrderCreate(BaseModel):
    items:List[OrderItemCreate]

class OrderItemResponse(BaseModel):
    id:int
    product_id:int
    quantity:int
    price:float
    class Config:
        from_attributes=True



class OrderResponse(BaseModel):
    id:int
    user_id:int
    status:str
    total_amount:float
    items:List[OrderItemResponse]=[]

    class Config:
        from_attributes=True