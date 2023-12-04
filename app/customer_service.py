from fastapi import HTTPException


# CRUD operations for customer
def create_customer(db, fname: str, lname: str, email: str, address: str, phone: int, status: str):
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("INSERT INTO CUSTOMER (FNAME, LNAME, EMAIL, ADDRESS, PHONE, STATUS) VALUES (%s, %s, %s, %s, %s, %s)", (fname, lname, email, address, phone, status))
        db.commit()
        customer_id = cursor.lastrowid
        return customer_id
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create user. {str(e)}")
    finally:
        cursor.close()


def get_customer_by_email(db, email: str):
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM CUSTOMER WHERE EMAIL = %s", (email,))
        customer = cursor.fetchone()
        return customer
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve user. {str(e)}")
    finally:
        cursor.close()


