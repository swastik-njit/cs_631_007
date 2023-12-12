from fastapi import HTTPException
from loguru import logger


def create_query(params):
    query = "UPDATE PRODUCT SET"
    for attribute in params:
        query += " "+ attribute + " = %s,"
    query = query[:-1] + " WHERE PID = %s"
    return query


# CRUD operations for products 
def add_to_basket(db, customer_id: int, product_id: int, quantity: int):
    # create new basket 
    # basket_id = None
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("INSERT INTO BASKET (CID) SELECT CID FROM CUSTOMER WHERE CID = %s AND NOT EXISTS (SELECT CID FROM BASKET WHERE CID = %s)", (customer_id, customer_id))
        db.commit()
        basket_id = cursor.lastrowid
        # return basket_id
        # add product to basket 
        try:
            cursor.execute('SELECT STATUS FROM CUSTOMER WHERE CID = %s', (customer_id))
            customer_status = cursor.fetchone()
            if customer_status == 'Gold' or customer_status == 'Platinum':
                cursor.execute("SELECT OFFERPRICE FROM OFFER_PRODUCT WHERE PID = %s", (product_id))
                product_price = cursor.fetchone()
            else:
                cursor.execute("SELECT PPRICE FROM PRODUCT WHERE PID = %s", (product_id))
                product_price = cursor.fetchone()
            cursor.execute("INSERT INTO APPEARS_IN (BID, PID, QUANTITY, PRICESOLD) VALUES (%s, %s, %s, %s)", (basket_id, product_id, quantity, product_price))
            db.commit()
            rows_affected = cursor.rowcount
            return basket_id, rows_affected
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Failed to add product to basket {basket_id} for customer... {str(e)}")
        finally:
            cursor.close()

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create basket for customer... {str(e)}")
    finally:
        cursor.close()
    

def update_basket(db, customer_id: int, product_id: int, quantity: int):
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM BASKET WHERE CID = %s", (customer_id))
        basket = cursor.fetchone()
        basket_id = basket['BID']

        try:
            cursor.execute('SELECT STATUS FROM CUSTOMER WHERE CID = %s', (customer_id))
            customer_status = cursor.fetchone()
            if customer_status == 'Gold' or customer_status == 'Platinum':
                cursor.execute("SELECT OFFERPRICE FROM OFFER_PRODUCT WHERE PID = %s", (product_id))
                product_price = cursor.fetchone()
            else:
                cursor.execute("SELECT PPRICE FROM PRODUCT WHERE PID = %s", (product_id))
                product_price = cursor.fetchone()
            cursor.execute("UPDATE APPEARS_IN (PID, QUANTITY, PRICESOLD) VALUES (%s, %s, %s) WHERE BID = %s", (basket_id, product_id, quantity, product_price))
            db.commit()
            rows_affected = cursor.rowcount
            return basket_id, rows_affected
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Failed to add product to basket {basket_id} for customer... {str(e)}")
        finally:
            cursor.close()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update product {product_id} in table... {str(e)}")
    finally:
        cursor.close()


def remove_basket(db, customer_id: int):
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("DELETE FROM BASKET WHERE CID = %s", customer_id)
        db.commit()
        rows_affected = cursor.rowcount
        return rows_affected
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to remove basket from table... {str(e)}")
    finally:
        cursor.close()


def get_basket_details(db, customer_id: int):
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM BASKET WHERE CID = %s", (customer_id))
        basket = cursor.fetchone()
        basket_id = basket['BID']
        cursor.execute("SELECT * FROM APPEARS_IN WHERE BID = %s", (basket_id,))
        basket = cursor.fetchall()
        return basket
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve basket {basket_id} details from table... {str(e)}")
    finally:
        cursor.close()


