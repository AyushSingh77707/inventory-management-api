from celery import Celery
import os

redis_url = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")

celery_app=Celery(
    "inventory_app",          #celery app's name
    broker=redis_url,        #redis pe queue
    backend=redis_url,       #result redis me save hoga
    include=["app.tasks"]     #hmare task yaha hai
)