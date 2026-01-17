from data.db import get_connection

class ProductService:
    def list(self):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT p.id, p.name, p.price, p.stock, c.name as category
            FROM products p JOIN categories c ON p.category_id=c.id
        """)
        products = cursor.fetchall()
        cursor.close()
        conn.close()
        return products
    
    def list_by_category(self, category_name):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT p.*, c.name as category 
            FROM products p
            JOIN categories c ON p.category_id = c.id
            WHERE c.name=%s
            """,
            (category_name,)
        )
        products = cursor.fetchall()
        cursor.close()
        conn.close()
        return products


    def add(self, name, price, stock, category_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("INSERT INTO products (name, price, stock, category_id) VALUES (%s, %s, %s, %s)",
                       (name, price, stock, category_id))
        conn.commit()
        product_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return {"id": product_id, "name": name, "price": price, "stock": stock, "category_id": category_id}

    def get(self, product_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT p.id, p.name, p.price, p.stock, c.name as category
            FROM products p JOIN categories c ON p.category_id=c.id
            WHERE p.id=%s
        """, (product_id,))
        product = cursor.fetchone()
        cursor.close()
        conn.close()
        return product

    def update(self, product_id, name=None, price=None, stock=None):
        conn = get_connection()
        cursor = conn.cursor()
        updates = []
        values = []
        if name:
            updates.append("name=%s")
            values.append(name)
        if price is not None:
            updates.append("price=%s")
            values.append(price)
        if stock is not None:
            updates.append("stock=%s")
            values.append(stock)
        values.append(product_id)
        cursor.execute(f"UPDATE products SET {', '.join(updates)} WHERE id=%s", tuple(values))
        conn.commit()
        cursor.close()
        conn.close()
