from fastapi import FastAPI
from app.database import engine,Base
from app.models import user,product,order

from app.routers import auth
from app.routers import product
from app.routers import order

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

Base.metadata.create_all(bind=engine)

app=FastAPI(title="Inventory Management API",description="Multi-tenant inventory system",version="1.0.0")
app.include_router(auth.router)
app.include_router(product.router)
app.include_router(order.router)

#redis setup
@app.on_event("startup")
async def startup():
    redis=aioredis.from_url("redis://localhost:6379")
    FastAPICache.init(RedisBackend(redis),prefix="cache")



@app.get("/health")
def health_check():
    return{"message":"api is running"}  

