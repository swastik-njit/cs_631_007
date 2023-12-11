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

@router.post("/add/")
async def create_product_route(customer_email: str = Form(...), product_id: int = Form(...), quantity: int = Form(...), db: mysql.connector.MySQLConnection = Depends(get_db)):
    customer = get_customer_by_email(db, customer_email)
    int(customer['CID'])

    basket_id = add_to_basket(db, customer_email, product_id, quantity)
    return JSONResponse(content={"product_id": product_id, "product_name": name, "price": price}, status_code=201)


# @router.post("/update/")
# async def create_product_route(product_id: int = Form(...), ptype: str = Form(Optional), name: str = Form(Optional), price: float = Form(Optional), desc: str = Form(Optional), quantity: int = Form(Optional), db: mysql.connector.MySQLConnection = Depends(get_db)):
    
#     product_details = {'PTYPE': ptype, 'PNAME': name, 'PPRICE': price, 'DESCRIPTION': desc, 'PQUANTITY': quantity}
#     product_details = {key: value for key, value in product_details.items() if (isinstance(value, int) or isinstance(value, float) or isinstance(value, str))}
#     product_details = {key: value for key, value in product_details.items() if (value != '' or value != 0)}
    
#     rows_affected = update_product(db, product_id, product_details)
#     return JSONResponse(content={"rows_affected": rows_affected, "product_id": product_id}, status_code=201)


@router.get("/get-all/")
async def get_products_route(db: mysql.connector.MySQLConnection = Depends(get_db)):
    products = get_all_products(db)
    return products


@router.get("/get-product/")
async def get_products_route(product_id: int, db: mysql.connector.MySQLConnection = Depends(get_db)):
    products = get_product(db, product_id)
    return products


