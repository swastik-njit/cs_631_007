import mysql.connector
from fastapi import APIRouter, Depends
from fastapi import Depends, HTTPException, Form
from fastapi.responses import JSONResponse
from typing import Optional
from loguru import logger

from .database import get_db
from .basket_service import add_to_basket
from .basket_service import update_basket
from .basket_service import remove_basket
from .basket_service import get_basket_details
from .customer_service import get_customer_by_email


router = APIRouter(prefix="/basket", tags=["Basket"])    

@router.post("/create/")
async def create_basket_route(customer_email: str = Form(...), product_id: int = Form(...), quantity: int = Form(...), db: mysql.connector.MySQLConnection = Depends(get_db)):
    customer = get_customer_by_email(db, customer_email)

    basket_id, rows_affected = add_to_basket(db, int(customer['CID']), product_id, quantity)
    return JSONResponse(content={"basket_id": basket_id, "rows_affected": rows_affected}, status_code=201)


@router.post("/update/")
async def update_basket_route(customer_email: str = Form(...), product_id: int = Form(...), quantity: int = Form(...), db: mysql.connector.MySQLConnection = Depends(get_db)):
    customer = get_customer_by_email(db, customer_email)
    int(customer['CID'])

    basket_id, rows_affected = update_basket(db, int(customer['CID']), product_id, quantity)
    return JSONResponse(content={"basket_id": basket_id, "rows_affected": rows_affected}, status_code=201)


@router.get("/remove/")
async def remove_basket_route(customer_email: str = Form(...), db: mysql.connector.MySQLConnection = Depends(get_db)):
    customer = get_customer_by_email(db, customer_email)

    rows_affected = remove_basket(db, int(customer['CID']))
    return JSONResponse(content={"rows_affected": rows_affected}, status_code=201)


@router.get("/get-details/")
async def get_basket_route(customer_email: str = Form(...), db: mysql.connector.MySQLConnection = Depends(get_db)):
    customer = get_customer_by_email(db, customer_email)

    basket_info = get_basket_details(db, int(customer['CID']))
    return JSONResponse(content={"basket_info": basket_info}, status_code=201)


