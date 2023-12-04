import mysql.connector
from fastapi import APIRouter, Depends
from fastapi import Depends, HTTPException, Form
from fastapi.responses import JSONResponse
from loguru import logger

from .config import config
from .database import get_db
from .order_service import create_order
from .order_service import get_orders
from .order_service import get_orders_by_user


router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/create-orders/")
async def create_order_route(user_id: int = Form(...), product_id: int = Form(...), quantity: int = Form(...), db: mysql.connector.MySQLConnection = Depends(get_db)):
    order_id = create_order(db, user_id, product_id, quantity)
    return JSONResponse(content={"order_id": order_id, "user_id": user_id, "product_id": product_id, "quantity": quantity}, status_code=201)


@router.get("/get-orders/")
async def get_orders_route(db: mysql.connector.MySQLConnection = Depends(get_db)):
    orders = get_orders(db)
    return orders

