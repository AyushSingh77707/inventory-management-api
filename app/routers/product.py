from fastapi import APIRouter,Depends,HTTPException
from app.schemas.product import ProductResponse,ProductCreate,ProductUpdate
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.dependencies import get_current_user,admin_only
from app.models.product import Product

router=APIRouter(prefix="/products",tags=["Products"])

@router.get("/")
def get_products(db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    data=db.query(Product).all()
    return data

@router.get("/{product_id}",response_model=ProductResponse)
def get_product(product_id:int,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    data=db.query(Product).filter(Product.id==product_id).first()
    if not data:
        raise HTTPException(status_code=404,detail=f"Product of product id {product_id} does not exist")
    return data

@router.post("/create",response_model=ProductResponse)
def create_product(productdata:ProductCreate,db:Session=Depends(get_db),current_user=Depends(admin_only)):
    new_product=Product(**productdata.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@router.put("/update/{product_id}",response_model=ProductResponse)
def update_product(product_id:int,product_data:ProductUpdate,db:Session=Depends(get_db),current_user=Depends(admin_only)):
    data=db.query(Product).filter(Product.id==product_id).first()
    if not data:
        raise HTTPException(status_code=404,detail=f"Product of product id {product_id} does not exist")
    
    for key,value in product_data.model_dump(exclude_unset=True).items():
        setattr(data,key,value)

    db.commit()
    db.refresh(data)
    return data

@router.delete("/delete/{product_id}")
def del_product(product_id:int,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    data=db.query(Product).filter(Product.id==product_id).first()
    if not data:
        raise HTTPException(status_code=404,detail=f"Product of product id {product_id} does not exist")
    db.delete(data)
    db.commit()
    return{"message":"Product deleted successfully from our database!"}




