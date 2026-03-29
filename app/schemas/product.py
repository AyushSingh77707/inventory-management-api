from pydantic import BaseModel,Field
from typing import Optional,Annotated

class ProductCreate(BaseModel):
    name:Annotated[str,Field(title="Enter product name here")]
    category:Annotated[str,Field(title="Enter category of product")]
    description:Annotated[Optional[str],Field(title="Enter description of product")]
    stock_quantity:Annotated[int,Field(title="Enter stock quantity")]
    price:Annotated[float,Field(ge=0,title="Enter price of product")]

class ProductUpdate(BaseModel):
    name:Optional[str]=None
    category:Optional[str]=None
    description:Optional[str]=None
    stock_quantity:Optional[int]=None
    price:Optional[float]=None

class ProductResponse(BaseModel):
    id:int
    name:str
    description:Optional[str]
    price:float
    stock_quantity:int
    category:str

    class Config:
        from_attributes=True