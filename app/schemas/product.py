from pydantic import BaseModel,Field
from typing import Optional,Annotated
from decimal import Decimal
from datetime import datetime
from app.models.product import CategoryEnum


class ProductCreate(BaseModel):
    name:Annotated[str,Field(title="Enter product name here")]
    category:Annotated[CategoryEnum,Field(title="Enter category of product",min_length=3)]
    description:Annotated[Optional[str],Field(title="Enter description of product",max_length=100)]
    stock_quantity:Annotated[int,Field(ge=0,title="Enter stock quantity")]
    price:Annotated[Decimal,Field(ge=0,title="Enter price of product")]

class ProductUpdate(BaseModel):
    name:Optional[str]=None
    category:Optional[CategoryEnum]=None
    description:Optional[str]=None
    stock_quantity:Annotated[Optional[int],Field(default=None,ge=0)]
    price:Annotated[Optional[Decimal],Field(default=None,ge=0)]

class ProductResponse(BaseModel):
    id:int
    name:str
    description:Optional[str]
    price:Decimal
    stock_quantity:int
    category:str
    is_active:bool
    updated_at:Optional[datetime]


    class Config:
        from_attributes=True