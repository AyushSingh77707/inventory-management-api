from celery import Celery

celery_app=Celery(
    "inventory_app",                          #celery app's name
    broker="redis://localhost:6379/0",        #redis pe queue
    backend="redis://localhost:6379/0",       #result redis me save hoga
    include=["app.tasks"]                     #hmare task yaha hai
)