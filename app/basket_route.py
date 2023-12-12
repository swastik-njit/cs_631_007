import mysql.connector
from fastapi import APIRouter, Depends
from fastapi import Depends, HTTPException, Form
from fastapi.responses import JSONResponse
from typing import Optional
from loguru import logger

from .database import get_db
from .basket_service import create_basket
from .basket_service import add_to_basket
from .basket_service import update_basket
from .basket_service import remove_basket
from .basket_service import get_basket_details
from .basket_service import get_all_baskets
from .basket_service import get_basket_item
from .customer_service import get_customer_by_email
from .product_service import update_product_quantity
from .product_service import get_product


router = APIRouter(prefix="/basket", tags=["Basket"])    

@router.post("/create/")
async def create_new_basket_route(customer_email: str = Form(...), db: mysql.connector.MySQLConnection = Depends(get_db)):
    customer = get_customer_by_email(db, customer_email)
    basket_id = create_basket(db, int(customer['CID']))
    return JSONResponse(content={"basket_id": basket_id}, status_code=201)


@router.post("/add-to-basket/")
async def add_product_to_basket(customer_email: str = Form(...), basket_id: int = Form(...), product_id: int = Form(...), quantity: int = Form(...), db: mysql.connector.MySQLConnection = Depends(get_db)):
    customer = get_customer_by_email(db, customer_email)
    rows_affected = add_to_basket(db, int(customer['CID']), basket_id, product_id, quantity)

    if rows_affected != 0:
        previous_quantity = get_product(db, product_id)
        previous_quantity = previous_quantity["PQUANTITY"]
        update_product_quantity(db, product_id, previous_quantity - quantity)

    return JSONResponse(content={"rows_affected": rows_affected}, status_code=201)


@router.post("/update/")
async def update_basket_route(customer_email: str = Form(...), basket_id: int = Form(...), product_id: int = Form(...), quantity: int = Form(...), db: mysql.connector.MySQLConnection = Depends(get_db)):
    customer = get_customer_by_email(db, customer_email)
    previous_quantity = get_basket_item(db, int(customer['CID']), basket_id, product_id)
    previous_quantity = previous_quantity["PQUANTITY"]
    rows_affected = update_basket(db, int(customer['CID']), basket_id, product_id, quantity)

    if rows_affected != 0:
        update_product_quantity(db, product_id, previous_quantity - quantity)

    return JSONResponse(content={"rows_affected": rows_affected}, status_code=201)


@router.post("/delete/")
async def remove_basket_route(customer_email: str = Form(...), basket_id: int = Form(...), db: mysql.connector.MySQLConnection = Depends(get_db)):
    customer = get_customer_by_email(db, customer_email)
    rows_affected = remove_basket(db, int(customer['CID']), basket_id)
    return JSONResponse(content={"rows_affected": rows_affected}, status_code=201)


@router.get("/get-details/")
async def get_basket_route(customer_email: str, basket_id: int, db: mysql.connector.MySQLConnection = Depends(get_db)):
    customer = get_customer_by_email(db, customer_email)
    basket_info = get_basket_details(db, int(customer['CID']), basket_id)
    return JSONResponse(content={"basket_info": basket_info}, status_code=201)


@router.get("/get-all-basket-details/")
async def get_basket_route(customer_email: str, db: mysql.connector.MySQLConnection = Depends(get_db)):
    customer = get_customer_by_email(db, customer_email)
    basket_info = get_all_baskets(db, int(customer['CID']))
    return JSONResponse(content={"basket_info": basket_info}, status_code=201)


