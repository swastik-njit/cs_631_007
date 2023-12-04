import mysql.connector
from fastapi import APIRouter, Depends
from fastapi import Depends, HTTPException, Form
from fastapi.responses import JSONResponse
from typing import Optional
from loguru import logger

from .database import get_db
from .shipping_service import add_new_ship_address
from .shipping_service import update_ship_address
from .shipping_service import delete_ship_address
from .shipping_service import get_customer_ship_address
from .shipping_service import get_ship_address_details
from .customer_service import get_customer_by_email


router = APIRouter(prefix="/shipping", tags=["Shipping Address"])

@router.post("/add-address/")
async def add_new_ship_addrs(customer_email: str = Form(...), saname: str = Form(...), recipient_name: str = Form(...), street: str = Form(...), snumber: str = Form(...), city: str = Form(...), zipcode: int = Form(...), state: str = Form(...), country: str = Form(...), db: mysql.connector.MySQLConnection = Depends(get_db)):
    customer = get_customer_by_email(db, customer_email)
    rows_affected = add_new_ship_address(db, customer['CID'], saname, recipient_name, street, snumber, city, zipcode, state, country)
    return JSONResponse(content={"rows_affected": rows_affected, "ship_address_name": saname, "recipient_name": recipient_name}, status_code=201)


@router.post("/update-address/")
async def update_ship_addrs(customer_email: str = Form(...), saname: str = Form(...), recipient_name: str = Form(Optional), street: str = Form(Optional), snumber: str = Form(Optional), city: str = Form(Optional), zipcode: int = Form(Optional), state: str = Form(Optional), country: str = Form(Optional), db: mysql.connector.MySQLConnection = Depends(get_db)):
    customer = get_customer_by_email(db, customer_email)
    
    addrs_details = {'RECEPIENTNAME': recipient_name, 'STREET': street, 'SNUMBER': snumber, 'CITY': city, 'ZIP': zipcode, 'STATE': state, 'COUNTRY': country}
    addrs_details = {key: value for key, value in addrs_details.items() if (isinstance(value, int) or isinstance(value, str))}
    addrs_details = {key: value for key, value in addrs_details.items() if (value != '' or value != 0)}

    rows_affected = update_ship_address(db, saname, customer['CID'], addrs_details)
    return JSONResponse(content={"rows_affected": rows_affected, "ship_address_name": saname, "recipient_name": recipient_name}, status_code=201)


@router.post("/delete-address/")
async def delete_ship_addrs(customer_email: str = Form(...), saname: str = Form(...), db: mysql.connector.MySQLConnection = Depends(get_db)):
    customer = get_customer_by_email(db, customer_email)
    rows_affected = delete_ship_address(db, customer['CID'], saname)

    if rows_affected == 0:
        raise HTTPException(status_code=401, detail="Invalid email provided")

    return JSONResponse(content={"Rows deleted": rows_affected}, status_code=201)


@router.get("/get-address/")
async def retrieve_customer_ship_address(customer_email: str, db: mysql.connector.MySQLConnection = Depends(get_db)):
    customer = get_customer_by_email(db, customer_email)
    addresses = get_customer_ship_address(db, customer['CID'])
    return JSONResponse(content={"addresses": addresses}, status_code=201)


@router.get("/get-details/")
async def retrieve_ship_address_details(customer_email: str, saname: str, db: mysql.connector.MySQLConnection = Depends(get_db)):
    customer = get_customer_by_email(db, customer_email)
    address = get_ship_address_details(db, customer['CID'], saname)
    return JSONResponse(content={"address_details": address}, status_code=201)

