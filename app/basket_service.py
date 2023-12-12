from fastapi import HTTPException
from loguru import logger


# CRUD operations for products 
def create_basket(db, customer_id: int):
    # create new basket 
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("INSERT INTO BASKET (CID) VALUES (%s)", (customer_id,))
        db.commit()
        basket_id = cursor.lastrowid
        return basket_id
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create basket for customer {customer_id}... {str(e)}")
    finally:
        cursor.close()


def add_to_basket(db, customer_id: int, basket_id: int, product_id: int, quantity: int):
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute('SELECT STATUS FROM CUSTOMER WHERE CID = %s', (customer_id,))
        customer_status = cursor.fetchone()
        customer_status = customer_status["STATUS"]
        
        if customer_status.lower() == 'gold' or customer_status.lower() == 'platinum':
            cursor.execute("SELECT OFFERPRICE FROM OFFER_PRODUCT WHERE PID = %s", (product_id,))
            product_price = cursor.fetchone()
            
            if product_price == None:
                cursor.execute("SELECT PPRICE FROM PRODUCT WHERE PID = %s", (product_id,))
                product_price = cursor.fetchone()
                product_price = product_price["PPRICE"]

            logger.debug("customer_status = {}", customer_status)
            logger.debug("OFFER Price = {}", product_price)
        else:
            cursor.execute("SELECT PPRICE FROM PRODUCT WHERE PID = %s", (product_id,))
            product_price = cursor.fetchone()
            product_price = product_price["PPRICE"]
        
        cursor.execute("INSERT INTO APPEARS_IN (BID, PID, QUANTITY, PRICESOLD) VALUES (%s, %s, %s, %s)", (basket_id, product_id, quantity, product_price))
        db.commit()
        rows_affected = cursor.rowcount
        return rows_affected
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to add product {product_id} to basket {basket_id} for customer {customer_id}... {str(e)}")
    finally:
        cursor.close()


def update_basket(db, customer_id: int, basket_id: int, product_id: int, quantity: int):
    cursor = db.cursor(dictionary=True)
    try:
        # cursor.execute('SELECT STATUS FROM CUSTOMER WHERE CID = %s', (customer_id))
        # customer_status = cursor.fetchone()
        # if customer_status == 'Gold' or customer_status == 'Platinum':
        #     cursor.execute("SELECT OFFERPRICE FROM OFFER_PRODUCT WHERE PID = %s", (product_id))
        #     product_price = cursor.fetchone()
        # else:
        #     cursor.execute("SELECT PPRICE FROM PRODUCT WHERE PID = %s", (product_id))
        #     product_price = cursor.fetchone()
        
        if quantity == 0:
            cursor.execute("DELETE FROM APPEARS_IN WHERE BID = %s AND PID = %s", (basket_id, product_id))
        else:
            cursor.execute("UPDATE APPEARS_IN SET QUANTITY = %s WHERE BID = %s AND PID = %s", (quantity, basket_id, product_id))

        db.commit()
        rows_affected = cursor.rowcount
        return rows_affected
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update product {product_id} in basket {basket_id} for customer... {str(e)}")
    finally:
        cursor.close()


def remove_basket(db, customer_id: int, basket_id: int):
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("DELETE FROM BASKET WHERE BID = %s AND CID = %s", (basket_id, customer_id))
        db.commit()
        rows_affected = cursor.rowcount
        return rows_affected
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to remove basket {basket_id} from table... {str(e)}")
    finally:
        cursor.close()


def get_basket_details(db, customer_id: int, basket_id: int):
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM APPEARS_IN WHERE BID = %s", (basket_id,))
        basket = cursor.fetchall()
        return basket
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve basket {basket_id} details from table... {str(e)}")
    finally:
        cursor.close()


def get_basket_item(db, customer_id: int, basket_id: int, product_id: int):
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM APPEARS_IN WHERE BID = %s AND PID = %s", (basket_id, product_id))
        basket = cursor.fetchall()
        return basket
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve basket {basket_id} details from table... {str(e)}")
    finally:
        cursor.close()


def get_all_baskets(db, customer_id: int):
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM BASKET B JOIN APPEARS_IN A ON B.BID = A.BID WHERE B.CID = %s", (customer_id,))
        all_basket = cursor.fetchall()
        return all_basket
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve baskets details from table for customer {customer_id}... {str(e)}")
    finally:
        cursor.close()


