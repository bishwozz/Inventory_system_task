# app/utils/alert.py

def send_low_stock_alert(product):
    """
    Sends a low stock alert for a product.
    Replace this with email, Slack, or other integrations as needed.
    """
    print(f"[LOW STOCK ALERT] Product '{product.name}' has low stock: {product.stock} left.")
