import mysql.connector
from fastapi import APIRouter, Depends
from fastapi import Depends, HTTPException, Form
from fastapi.responses import JSONResponse
from typing import Optional
from loguru import logger

from .database import get_db
from .product_service import create_product
from .product_service import update_product
from .product_service import get_all_products
from .product_service import get_product


router = APIRouter(prefix="/product", tags=["Product"])    

@router.post("/add/")
async def create_product_route(ptype: str = Form(...), name: str = Form(...), price: float = Form(...), desc: str = Form(...), quantity: int = Form(...), offer_price: float = Form(...), db: mysql.connector.MySQLConnection = Depends(get_db)):
    # if isinstance(offer_price, float):

    product_id = create_product(db, ptype, name, price, desc, quantity, offer_price)
    return JSONResponse(content={"product_id": product_id, "product_name": name, "price": price}, status_code=201)


@router.post("/update/")
async def create_product_route(product_id: int = Form(...), ptype: str = Form(Optional), name: str = Form(Optional), price: float = Form(Optional), desc: str = Form(Optional), quantity: int = Form(Optional), db: mysql.connector.MySQLConnection = Depends(get_db)):
    
    product_details = {'PTYPE': ptype, 'PNAME': name, 'PPRICE': price, 'DESCRIPTION': desc, 'PQUANTITY': quantity}
    product_details = {key: value for key, value in product_details.items() if (isinstance(value, int) or isinstance(value, float) or isinstance(value, str))}
    product_details = {key: value for key, value in product_details.items() if (value != '' or value != 0)}
    
    rows_affected = update_product(db, product_id, product_details)
    return JSONResponse(content={"rows_affected": rows_affected, "product_id": product_id}, status_code=201)


@router.get("/get-all/")
async def get_products_route(db: mysql.connector.MySQLConnection = Depends(get_db)):
    products = get_all_products(db)
    return products


@router.get("/get-product/")
async def get_products_route(product_id: int, db: mysql.connector.MySQLConnection = Depends(get_db)):
    products = get_product(db, product_id)
    return products


