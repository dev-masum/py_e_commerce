from data.db import get_connection

class CartService:
    def get_cart(self, user_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT product_id, quantity FROM cart_items WHERE user_id=%s
        """, (user_id,))
        items = cursor.fetchall()
        cursor.close()
        conn.close()
        return items

    def add_item(self, user_id, product_id, quantity):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO cart_items (user_id, product_id, quantity)
                VALUES (%s,%s,%s)
                ON DUPLICATE KEY UPDATE quantity=quantity+VALUES(quantity)
            """, (user_id, product_id, quantity))
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    def remove_item(self, user_id, product_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cart_items WHERE user_id=%s AND product_id=%s", (user_id, product_id))
        conn.commit()
        cursor.close()
        conn.close()

    def clear_cart(self, user_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cart_items WHERE user_id=%s", (user_id,))
        conn.commit()
        cursor.close()
        conn.close()
