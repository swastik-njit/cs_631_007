import mysql.connector
from fastapi import APIRouter, Depends
from fastapi import Depends, HTTPException, Form
from fastapi.responses import JSONResponse
from loguru import logger

from .database import get_db
from .customer_service import create_customer
from .customer_service import get_customer_by_email


router = APIRouter(prefix="/customer", tags=["Customers"])

@router.post("/register/")
async def register(fname: str = Form(...), lname: str = Form(...), email: str = Form(...), address: str = Form(...), phone: int = Form(...), status: str = Form(...), db: mysql.connector.MySQLConnection = Depends(get_db)):
    user_id = create_customer(db, fname, lname, email, address, phone, status)
    return JSONResponse(content={"customer_id": user_id, "firstname": fname, "email_id": email, "status": status}, status_code=201)


@router.post("/login/")
async def login(email: str = Form(...), db: mysql.connector.MySQLConnection = Depends(get_db)):
    customer = get_customer_by_email(db, email)
    if not customer:
        raise HTTPException(status_code=401, detail="Invalid email provided")

    logger.debug("***********  User ID: {}", customer)
    return JSONResponse(content={'customer_details': customer})
    
