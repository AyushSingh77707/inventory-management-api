from app.celery_app import celery_app
#stock alert
@celery_app.task              #decorater telling that this function is a celery task
def stock_alert(order_items:list):
    print("background task has started!")

    for item in order_items:
        product_name=item["name"]
        stock=item["stock"]

        if stock<10:
            print(f"low stock alert of {product_name},only {stock} left!")
        else:
            print("stocks are sufficient...")

    print("Background Task completed.")
    return "Stock check done"