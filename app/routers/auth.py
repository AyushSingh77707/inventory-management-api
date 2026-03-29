from fastapi import APIRouter,Depends,HTTPException
from app.schemas.user import UserLogin,UserRegister,UserResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.core.security import hash_password,verify_password,create_access_token,verify_token

router=APIRouter(prefix="/auth",tags=["Authentication"])  #prefix of url and tags 

@router.post("/register",response_model=UserResponse)
def register(info:UserRegister,db:Session=Depends(get_db)):

    existing_user=db.query(User).filter(User.email==info.email).first()
    if existing_user:
        raise HTTPException(status_code=400,detail="Email already registered!")
    hashed=hash_password(info.password)

    new_user=User(name=info.name,email=info.email,password=hashed,role=info.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login")
def login(info:UserLogin,db:Session=Depends(get_db)):
    user=db.query(User).filter(User.email==info.email).first()
    
    if not user or not verify_password(info.password,user.password):
        raise HTTPException(status_code=401,detail="invalid email or password!")

    token=create_access_token(data={
        "sub":str(user.id),
        "role":user.role
    })

    return {
        "access token":token,
        "token type":"bearer",
        "user":{
            "name":user.name,
            "id":user.id,
            "role":user.role,
            "email":user.email
        },
        "message":"User Logged in successfully!"
    }
    
    
    
    
    
