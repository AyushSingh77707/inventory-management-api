from fastapi import APIRouter,Depends,HTTPException,Query
from app.schemas.product import ProductResponse,ProductCreate,ProductUpdate
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.dependencies import get_current_user,admin_only
from app.models.product import Product
from typing import Optional

from fastapi_cache.decorator import cache
from fastapi_cache import FastAPICache

router=APIRouter(prefix="/products",tags=["Products"])

# @router.get("/")
# def get_products(db:Session=Depends(get_db),current_user=Depends(get_current_user)):
#     data=db.query(Product).all()
#     return data

#pagination and filtering with caching
@router.get("/")
@cache(expire=120)
async def get_products(page:int=Query(default=1,ge=1),limit:int=Query(default=5,ge=1,le=50),category:Optional[str]=Query(default=None),db:Session=Depends(get_db),current_user=Depends(get_current_user),search:Optional[str]=Query(default=None),min_price:Optional[str]=Query(default=None),max_price:Optional[int]=Query(default=None)):

    query=db.query(Product).filter(Product.is_active==True)
    if category:
        query=query.filter(Product.category==category)
    if search:
        query=query.filter(Product.name.ilike(f"%{search}%"))
    if min_price:
        query=query.filter(Product.price>=min_price)
    if max_price:
        query=query.filter(Product.price<=max_price)

    offset=(page-1)*limit
    
    data=query.offset(offset).limit(limit).all()
    return data
    

@router.get("/{product_id}",response_model=ProductResponse)
def get_product(product_id:int,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    data=db.query(Product).filter(Product.id==product_id,Product.is_active==True).first()
    if not data:
        raise HTTPException(status_code=404,detail=f"Product of product id {product_id} does not exist")
    return data

@router.post("/create",response_model=ProductResponse)
async def create_product(productdata:ProductCreate,db:Session=Depends(get_db),current_user=Depends(admin_only)):
    new_product=Product(**productdata.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    await FastAPICache.clear(namespace="cache") #cache invalidation
    return new_product

@router.put("/update/{product_id}",response_model=ProductResponse)
async def update_product(product_id:int,product_data:ProductUpdate,db:Session=Depends(get_db),current_user=Depends(admin_only)):
    data=db.query(Product).filter(Product.id==product_id).first()
    if not data:
        raise HTTPException(status_code=404,detail=f"Product of product id {product_id} does not exist")
    
    for key,value in product_data.model_dump(exclude_unset=True).items():
        setattr(data,key,value)

    db.commit()
    db.refresh(data)

    await FastAPICache.clear(namespace="cache")
    return data

@router.delete("/delete/{product_id}")
async def del_product(product_id:int,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    data=db.query(Product).filter(Product.id==product_id).first()
    if not data:
        raise HTTPException(status_code=404,detail=f"Product of product id {product_id} does not exist")
    # db.delete(data)
    Product.is_active=False
    db.commit()

    await FastAPICache.clear(namespace="cache")
    return{"message":"Product deleted successfully from our database!"}




