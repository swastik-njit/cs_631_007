from fastapi import HTTPException
from loguru import logger


def create_query(params):
    query = "UPDATE PRODUCT SET"
    for attribute in params:
        query += " "+ attribute + " = %s,"
    query = query[:-1] + " WHERE PID = %s"
    return query


# CRUD operations for products
def create_product(db, ptype: str, name: str, price: float, desc: str, quantity: int):
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("INSERT INTO PRODUCT (PTYPE, PNAME, PPRICE, DESCRIPTION, PQUANTITY) VALUES (%s, %s, %s, %s, %s)", (ptype, name, price, desc, quantity))
        db.commit()
        product_id = cursor.lastrowid
        return product_id
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to add product {name} in table... {str(e)}")
    finally:
        cursor.close()


def add_product_offer(db, product_id: int, offer_price: float):
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("INSERT INTO OFFER_PRODUCT (PID, OFFERPRICE) VALUES (%s, %s)", (product_id, offer_price))
        db.commit()
        rows_affected = cursor.rowcount
        return rows_affected
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to add product offer price {offer_price} in table... {str(e)}")
    finally:
        cursor.close()


def update_product(db, product_id: int, product_details: dict):
    update_query = create_query(product_details)
    values = tuple(param for param in product_details.values()) + (product_id,)

    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute(update_query, values)
        db.commit()
        rows_affected = cursor.rowcount
        return rows_affected
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update product {product_id} in table... {str(e)}")
    finally:
        cursor.close()


def update_product_quantity(db, product_id: int, quantity: int):
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("UPDATE PRODUCT SET PQUANTITY = %s WHERE PID = %s;", (quantity, product_id))
        db.commit()
        rows_affected = cursor.rowcount
        return rows_affected
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update product {product_id} quantity in table... {str(e)}")
    finally:
        cursor.close()


def get_all_products(db):
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM PRODUCT")
        products = cursor.fetchall()
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve products from table... {str(e)}")
    finally:
        cursor.close()


def get_product(db, product_id: int):
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM PRODUCT WHERE PID = %s", (product_id,))
        product = cursor.fetchone()
        return product
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve product {product_id} from table... {str(e)}")
    finally:
        cursor.close()


