from passlib.context import CryptContext
from datetime import datetime,timedelta,timezone
from jose import jwt,JWTError
from app.core.config import settings
from fastapi import HTTPException

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")        #hashing engine

def hash_password(password:str):
    return pwd_context.hash(password)

def verify_password(plain:str,hashed:str):
    return pwd_context.verify(plain,hashed)

def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.now(timezone.utc)+timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode,settings.JWT_SECRET_KEY,algorithm=settings.JWT_ALGORITHM)

def verify_token(token:str)->dict:
    try:
        payload=jwt.decode(token,settings.JWT_SECRET_KEY,algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError as e:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

