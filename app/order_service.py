from fastapi import HTTPException


# CRUD operations for orders
def create_order(db, user_id: int, product_id: int, quantity: int):
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM products WHERE product_id = %s", (product_id,))
        product = cursor.fetchone()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        total_price = quantity * product["price"]
        cursor.execute("INSERT INTO orders (user_id, product_id, quantity, total_price) VALUES (%s, %s, %s, %s)",
                       (user_id, product_id, quantity, total_price))
        db.commit()
        order_id = cursor.lastrowid
        return order_id
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create order. {str(e)}")
    finally:
        cursor.close()


def get_orders_by_user(db, user_id: int):
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM orders WHERE user_id = %s", (user_id,))
        orders = cursor.fetchall()
        return orders
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve orders. {str(e)}")
    finally:
        cursor.close()


def get_orders(db):
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM orders")
        orders = cursor.fetchall()
        return orders
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve orders. {str(e)}")
    finally:
        cursor.close()


