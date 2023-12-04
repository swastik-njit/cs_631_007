from fastapi import HTTPException


def create_query(params):
    query = "UPDATE SHIPPING_ADDRESS SET"
    for attribute in params:
        query += " "+ attribute + " = %s,"
    query = query[:-1] + " WHERE SANAME = %s AND CID = %s"
    return query


# CRUD operations for credit cards
def add_new_ship_address(db, customer_id: int, saname: str, recipient_name: str, street: str, snumber: str, city: str, zipcode: int, state: str, country: str):
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("INSERT INTO SHIPPING_ADDRESS (CID, SANAME, RECEPIENTNAME, STREET, SNUMBER, CITY, ZIP, STATE, COUNTRY) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (customer_id, saname, recipient_name, street, snumber, city, zipcode, state, country))
        db.commit()
        rows_affected = cursor.rowcount
        return rows_affected
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create credit card. {str(e)}")
    finally:
        cursor.close()


def update_ship_address(db, saname: str, customer_id: int, addrs_details: dict):
    update_query = create_query(addrs_details)
    values = tuple(param for param in addrs_details.values()) + (saname, customer_id)

    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute(update_query, values)
        db.commit()
        rows_affected = cursor.rowcount
        return rows_affected
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update shipping address {saname} in table... {str(e)}")
    finally:
        cursor.close()


def delete_ship_address(db, customer_id: int, saname: str):
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("DELETE FROM SHIPPING_ADDRESS WHERE SANAME = %s AND CID = %s", (saname, customer_id))
        db.commit()
        rows_affected = cursor.rowcount
        return rows_affected
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete shipping address {saname} from table... {str(e)}")
    finally:
        cursor.close()


def get_customer_ship_address(db, customer_id: int):
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM SHIPPING_ADDRESS WHERE CID = %s", (customer_id,))
        card = cursor.fetchall()
        return card
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve shipping addres for customer id {customer_id} from table... {str(e)}")
    finally:
        cursor.close()


def get_ship_address_details(db, customer_id: int, saname: int):
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM SHIPPING_ADDRESS WHERE SANAME = %s AND CID = %s", (saname, customer_id))
        card = cursor.fetchone()
        return card
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve shipping address {saname} from table... {str(e)}")
    finally:
        cursor.close()


