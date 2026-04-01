from fastapi import APIRouter,Depends,HTTPException
from app.models.order import Order,OrderItem
from app.schemas.order import OrderCreate,OrderItemCreate,OrderResponse,OrderItemResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.dependencies import get_current_user,admin_only
from typing import List
from app.models.product import Product

from app.tasks import stock_alert

router=APIRouter(prefix="/orders",tags=["Orders"])

@router.post("/",response_model=OrderResponse)
def create_order(order_data:OrderCreate,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    total=0.0
    order_items=[]

    for i in order_data.items:
        product=db.query(Product).filter(Product.id==i.product_id).first()
        if not product:
            raise HTTPException(status_code=404,detail=f"product of {i.product_id} do not exist")
        if product.stock_quantity<i.quantity:
            raise HTTPException(status_code=400,detail=f"insufficient stock for {product.name}")
        total+=product.price*i.quantity
        order_items.append({
            "product_id":i.product_id,
            "quantity":i.quantity,
            "price":product.price
        })
        product.stock_quantity-=i.quantity

        new_order=Order(user_id=current_user.id,total_amount=total)
        db.add(new_order)
        db.flush()   #flush krne se sirf id mil rhi h new_order.id

        for item_data in order_items:
            order_item=OrderItem(order_id=new_order.id,**item_data)
            db.add(order_item)
        db.commit()
        db.refresh(new_order)

        #data collect
        items_for_check=[]
        for item in order_items:
            product=db.query(Product).filter(Product.id==item["product_id"]).first()
            items_for_check.append({"name":product.name,"stock":product.stock_quantity})
        stock_alert.delay(items_for_check)    
        return new_order

@router.get("/",response_model=List[OrderResponse])
def get_orders(db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    if current_user.role=="admin":
        return db.query(Order).all()
    return db.query(Order).filter(Order.user_id==current_user.id).all()

@router.get("/{order_id}",response_model=OrderResponse)
def get_order(order_id:int,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    data=db.query(Order).filter(Order.id==order_id).first()
    if not data:
        raise HTTPException(status_code=404,detail="Order Not Found!")
    if current_user.role!="admin" and data.user_id!=current_user.id:
        raise HTTPException(status_code=403,detail="Not authorised!")
    return data

@router.put("/{order_id}/status")
def update_status(order_id:int,status:str,db:Session=Depends(get_db),current_user=Depends(admin_only)):
    data=db.query(Order).filter(Order.id==order_id).first()
    if not data:
        raise HTTPException(status_code=404,detail="Order Not Found!")

    valid_status=["pending","delivered","processing","cancelled"]
    if status not in valid_status:
        raise HTTPException(status_code=400,detail="Invalid Status!")
    data.status=status
    db.commit()
    db.refresh(data)
    return {"message":f"Order status updated to {status}"}

        
    




        

    









