from fastapi import HTTPException
from loguru import logger


def create_query(params):
    query = "UPDATE CREDIT_CARD SET"
    for attribute in params:
        query += " "+ attribute + " = %s,"
    query = query[:-1] + " WHERE CCNUMBER = %s AND STOREDCARDCID = %s"
    return query


# CRUD operations for credit cards
def add_new_card(db, card_number: int, sec_number: int, owner_name: str, card_type: str, bill_addrs: str, exp_date: str, card_cid: int):
    cursor = db.cursor(dictionary=True)
    logger.debug("cid = {}", card_cid)
    try:
        cursor.execute("INSERT INTO CREDIT_CARD (CCNUMBER, SECNUMBER, OWNERNAME, CCTYPE, BILLADDRESS, EXPDATE, STOREDCARDCID) VALUES (%s, %s, %s, %s, %s, %s, %s)", (card_number, sec_number, owner_name, card_type, bill_addrs, exp_date, card_cid))
        db.commit()
        rows_affected = cursor.rowcount
        return rows_affected
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create credit card. {str(e)}")
    finally:
        cursor.close()


def update_cards(db, card_number: int, card_cid: int, card_details: dict):
    update_query = create_query(card_details)
    values = tuple(param for param in card_details.values()) + (card_number, card_cid)

    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute(update_query, values)
        db.commit()
        rows_affected = cursor.rowcount
        return rows_affected
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update credit card {card_number} in table... {str(e)}")
    finally:
        cursor.close()


def delete_cards(db, card_cid: int, card_number: int):
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("DELETE FROM CREDIT_CARD WHERE CCNUMBER = %s AND STOREDCARDCID = %s", (card_number, card_cid))
        db.commit()
        rows_affected = cursor.rowcount
        return rows_affected
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete credit card {card_number} from table... {str(e)}")
    finally:
        cursor.close()


def get_all_cards(db):
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM CREDIT_CARD")
        all_cards = cursor.fetchall()
        return all_cards
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve credit cards. {str(e)}")
    finally:
        cursor.close()


def get_customer_cards(db, card_cid: int):
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM CREDIT_CARD WHERE STOREDCARDCID = %s", (card_cid,))
        cards = cursor.fetchall()
        return cards
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve credit cards for customer id {card_cid} from table... {str(e)}")
    finally:
        cursor.close()


def get_card_details(db, card_cid: int, card_number: int):
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM CREDIT_CARD WHERE CCNUMBER = %s AND STOREDCARDCID = %s", (card_number, card_cid))
        card = cursor.fetchone()
        return card
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve credit card {card_number} from table... {str(e)}")
    finally:
        cursor.close()


