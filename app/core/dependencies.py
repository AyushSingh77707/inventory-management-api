from fastapi.security import OAuth2PasswordBearer
from app.core.security import verify_token
from fastapi import Depends,HTTPException
from app.database import get_db
from sqlalchemy.orm import Session
from app.models.user import User

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/auth/login")  #defines mechanism of extracting token from request,it is a dependency class which extract token from header of request and token url defines from where it has to be extracted

def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(get_db)):
    payload=verify_token(token)
    if not payload:
        raise HTTPException(status_code=401,detail="invalid token")
    user=db.query(User).filter(User.id==payload.get("sub")).first()
    return user

def admin_only(current_user=Depends(get_current_user)):
    if current_user.role!="admin":
        raise HTTPException(status_code=403,detail="admin only allowed")
    return current_user