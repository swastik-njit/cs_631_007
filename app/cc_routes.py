import json
import mysql.connector
from fastapi import APIRouter, Depends
from fastapi import Depends, HTTPException, Form
from fastapi.responses import JSONResponse
from typing import Optional
from loguru import logger
from dateutil.parser import parse

from .database import get_db
from .cc_service import add_new_card
from .cc_service import update_cards
from .cc_service import delete_cards
from .cc_service import get_all_cards
from .cc_service import get_card_details
from .cc_service import get_customer_cards
from .customer_service import get_customer_by_email


router = APIRouter(prefix="/credit-cards", tags=["Credit Cards"])

@router.post("/add/")
async def add(customer_email: str = Form(...), card_number: int = Form(...), sec_number: int = Form(...), owner_name: str = Form(...), card_type: str = Form(...), bill_addrs: str = Form(...), exp_date: str = Form(...), db: mysql.connector.MySQLConnection = Depends(get_db)):
    customer = get_customer_by_email(db, customer_email)

    try:
        exp_date = parse(exp_date).strftime("%Y-%m-%d")
    except Exception as e:
        logger.error("Cannot convert to date format")

    rows_affected = add_new_card(db, card_number, sec_number, owner_name, card_type, bill_addrs, exp_date, int(customer['CID']))
    return JSONResponse(content={"rows_affected": rows_affected, "card_number": card_number, "owner_name": owner_name}, status_code=201)


@router.post("/update/")
async def update(customer_email: str = Form(...), card_number: int = Form(...), sec_number: int = Form(Optional), owner_name: str = Form(Optional), card_type: str = Form(Optional), bill_addrs: str = Form(Optional), exp_date: str = Form(Optional), db: mysql.connector.MySQLConnection = Depends(get_db)):
    customer = get_customer_by_email(db, customer_email)
    
    try:
        exp_date = parse(exp_date).strftime("%Y-%m-%d")
    except Exception as e:
        logger.error("Cannot convert to date format")

    card_details = {'SECNUMBER': sec_number, 'OWNERNAME': owner_name, 'CCTYPE': card_type, 'BILLADDRESS': bill_addrs, 'EXPDATE': exp_date}
    card_details = {key: value for key, value in card_details.items() if (isinstance(value, int) or isinstance(value, str))}
    card_details = {key: value for key, value in card_details.items() if (value != '' or value != 0)}

    rows_affected = update_cards(db, card_number, int(customer['CID']), card_details)
    return JSONResponse(content={"rows_affected": rows_affected, "card_number": card_number}, status_code=201)


@router.post("/delete/")
async def delete(customer_email: str = Form(...), card_number: int = Form(...), db: mysql.connector.MySQLConnection = Depends(get_db)):
    customer = get_customer_by_email(db, customer_email)
    rows_affected = delete_cards(db, int(customer['CID']), card_number)

    if rows_affected == 0:
        raise HTTPException(status_code=401, detail="Invalid email provided")

    return JSONResponse(content={"Rows deleted": rows_affected}, status_code=201)


@router.get("/get-all/")
async def retrieve_all_cards(db: mysql.connector.MySQLConnection = Depends(get_db)):
    cards = get_all_cards(db)
    return JSONResponse(content=json.dumps({"all_cards": cards}, default=str), status_code=201)


@router.get("/get-customer/")
async def retrieve_customer_cards(customer_email: str, db: mysql.connector.MySQLConnection = Depends(get_db)):
    customer = get_customer_by_email(db, customer_email)
    cards = get_customer_cards(db, int(customer['CID']))
    return JSONResponse(content=json.dumps({"cards": cards}, default=str), status_code=201)


@router.get("/get-details/")
async def retrieve_card_details(customer_email: str, card_number: int, db: mysql.connector.MySQLConnection = Depends(get_db)):
    customer = get_customer_by_email(db, customer_email)
    card = get_card_details(db, int(customer['CID']), card_number)
    return JSONResponse(content=json.dumps({"card_details": card}, default=str), status_code=201)



