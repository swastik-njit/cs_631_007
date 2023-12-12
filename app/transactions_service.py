from fastapi import HTTPException


# CRUD operations for orders
def create_transaction(db, customer_id: int, basket_id: int, card_num: int, ship_name: str, transaction_date: str, transaction_tag: str):
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("INSERT INTO TRANSACTION (BID, CCNUMBER, CID, SANAME, TDATE, TTAG) VALUES (%s, %s, %s, %s, %s, %s)", (basket_id, card_num, customer_id, ship_name, transaction_date, transaction_tag))
        db.commit()
        rows_affected = cursor.rowcount
        return rows_affected
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create new order transaction... {str(e)}")
    finally:
        cursor.close()


def update_transaction(db, customer_id: int, basket_id: int, card_num: int, ship_name: str, transaction_tag: str):
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("UPDATE TRANSACTION SET TTAG = %s WHERE BID = %s AND CCNUMBER = %s AND CID = %s AND SANAME = %s", (transaction_tag, basket_id, card_num, customer_id, ship_name))
        db.commit()
        rows_affected = cursor.rowcount
        return rows_affected
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update the order transaction... {str(e)}")
    finally:
        cursor.close()


def get_transactions_by_customer(db, customer_id: int):
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM TRANSACTION WHERE CID = %s", (customer_id,))
        transaction = cursor.fetchall()
        return transaction
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve order transactions... {str(e)}")
    finally:
        cursor.close()


def get_transactions(db):
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM TRANSACTION")
        transactions = cursor.fetchall()
        return transactions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve order transactions... {str(e)}")
    finally:
        cursor.close()


