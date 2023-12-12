import mysql.connector
from fastapi import APIRouter, Depends
from fastapi import Depends, HTTPException, Form
from fastapi.responses import JSONResponse
from datetime import datetime
from loguru import logger

from .config import config
from .database import get_db
from .transactions_service import create_transaction
from .transactions_service import update_transaction
from .transactions_service import get_transactions
from .transactions_service import get_transactions_by_customer
from .customer_service import get_customer_by_email


router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.post("/create/")
async def create_transaction_route(customer_email: str = Form(...), basket_id: int = Form(...), card_num: int = Form(...), ship_name: str = Form(...), db: mysql.connector.MySQLConnection = Depends(get_db)):
    customer = get_customer_by_email(db, customer_email)
    transaction_date = datetime.today().strftime('%Y-%m-%d')
    transaction_tag = "ORDER PLACED"
    rows_affected = create_transaction(db, int(customer['CID']), basket_id, card_num, ship_name, transaction_date, transaction_tag)
    return JSONResponse(content={"basket_id": basket_id, "customer_id": int(customer['CID']), "rows_affected": rows_affected}, status_code=201)


@router.post("/update/")
async def update_transaction_route(customer_email: str = Form(...), basket_id: int = Form(...), card_num: int = Form(...), ship_name: str = Form(...), transaction_status: str = Form(...), db: mysql.connector.MySQLConnection = Depends(get_db)):
    customer = get_customer_by_email(db, customer_email)
    rows_affected = update_transaction(db, int(customer['CID']), basket_id, card_num, ship_name, transaction_status)
    return JSONResponse(content={"basket_id": basket_id, "customer_id": int(customer['CID']), "rows_affected": rows_affected}, status_code=201)


@router.get("/get-customer/")
async def get_customer_transactions_route(customer_email: str, db: mysql.connector.MySQLConnection = Depends(get_db)):
    customer = get_customer_by_email(db, customer_email)
    transactions = get_transactions_by_customer(db, int(customer['CID']))
    return transactions


@router.get("/get-all/")
async def get_all_transactions_route(db: mysql.connector.MySQLConnection = Depends(get_db)):
    transactions = get_transactions(db)
    return transactions

