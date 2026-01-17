from data.db import get_connection

class ProductService:
    # List all products
    def list(self):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT p.id, p.name, p.price, p.stock, p.image_url, p.description, c.name as category
            FROM products p 
            JOIN categories c ON p.category_id=c.id
        """)
        products = cursor.fetchall()
        cursor.close()
        conn.close()
        return products

    # List products filtered by category
    def list_by_category(self, category_name):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT p.id, p.name, p.price, p.stock, p.image_url, p.description, c.name as category
            FROM products p
            JOIN categories c ON p.category_id = c.id
            WHERE c.name=%s
        """, (category_name,))
        products = cursor.fetchall()
        cursor.close()
        conn.close()
        return products

    # Add a new product
    def add(self, name, price, stock, category_id, image_url=None, description=None):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            INSERT INTO products (name, price, stock, category_id, image_url, description)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (name, price, stock, category_id, image_url, description)
        )
        conn.commit()
        product_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return {
            "id": product_id,
            "name": name,
            "price": price,
            "stock": stock,
            "category_id": category_id,
            "image_url": image_url,
            "description": description
        }

    # Get a single product by ID
    def get(self, product_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT p.id, p.name, p.price, p.stock, p.image_url, p.description, c.name as category
            FROM products p 
            JOIN categories c ON p.category_id=c.id
            WHERE p.id=%s
        """, (product_id,))
        product = cursor.fetchone()
        cursor.close()
        conn.close()
        return product

    # Update an existing product
    def update(self, product_id, name=None, price=None, stock=None, image_url=None, description=None):
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
        if image_url is not None:
            updates.append("image_url=%s")
            values.append(image_url)
        if description is not None:
            updates.append("description=%s")
            values.append(description)

        if updates:  # Only run update if there are fields to update
            values.append(product_id)
            cursor.execute(f"UPDATE products SET {', '.join(updates)} WHERE id=%s", tuple(values))
            conn.commit()

        cursor.close()
        conn.close()

    # Delete a product
    def delete(self, product_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE id=%s", (product_id,))
        conn.commit()
        cursor.close()
        conn.close()
