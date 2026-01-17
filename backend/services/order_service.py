from data.db import get_connection

class OrderService:
    def place_order(self, user_id, cart_items, total_price):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        # Insert into orders
        cursor.execute("INSERT INTO orders (user_id, total_price) VALUES (%s,%s)", (user_id, total_price))
        order_id = cursor.lastrowid
        # Insert order items
        for item in cart_items:
            cursor.execute("INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (%s,%s,%s,%s)",
                           (order_id, item["product_id"], item["quantity"], item["price"]))
        conn.commit()
        cursor.close()
        conn.close()
        return {"id": order_id, "products": cart_items, "total_price": total_price, "user_id": user_id}

    def get_orders(self, user_id=None):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        if user_id:
            cursor.execute("SELECT * FROM orders WHERE user_id=%s", (user_id,))
        else:
            cursor.execute("SELECT * FROM orders")
        
        orders = cursor.fetchall()
    
        for order in orders:
            cursor.execute("""
                SELECT oi.product_id, p.name AS product_name, oi.quantity, oi.price
                FROM order_items oi
                JOIN products p ON oi.product_id = p.id
                WHERE oi.order_id=%s
            """, (order["id"],))
            order["products"] = cursor.fetchall()
        
        cursor.close()
        conn.close()

        return orders
    
    