from fastapi import FastAPI
from app.database import engine,Base
from app.models.user import User

from app.routers import auth

Base.metadata.create_all(bind=engine)

app=FastAPI(title="Inventory Management API",description="Multi-tenant inventory system",version="1.0.0")
app.include_router(auth.router)



@app.get("/health")
def health_check():
    return{"message":"api is running"}  

