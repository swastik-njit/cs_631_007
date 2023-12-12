import mysql.connector
from fastapi import APIRouter, Depends
from fastapi import Depends, HTTPException, Form
from fastapi.responses import JSONResponse
from datetime import datetime
from loguru import logger
from dateutil.parser import parse

from .config import config
from .database import get_db


router = APIRouter(prefix="/sales-info", tags=["Sales Statistics"])

@router.get("/stats-1/", tags=["stats-1"])
async def sale_stats_1(db: mysql.connector.MySQLConnection = Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT CCNUMBER, SUM(TOTAL_COST) FROM TRANSACTION T, (SELECT BID, SUM(QUANTITY*PRICESOLD) AS TOTAL_COST FROM APPEARS_IN GROUP BY BID) IT WHERE T.BID = IT.BID GROUP BY CCNUMBER")
        response = cursor.fetchall()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to fetch details from database... {str(e)}")
    finally:
        cursor.close()

    return response


@router.get("/stats-2/", tags=["stats-2"])
async def sale_stats_2(db: mysql.connector.MySQLConnection = Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT C.FNAME, C.LNAME, SUM(TOTAL_COST) FROM CUSTOMER C, TRANSACTION T, (SELECT BID, SUM(QUANTITY*PRICESOLD) AS TOTAL_COST FROM APPEARS_IN GROUP BY BID) IT WHERE C.CID = T.CID AND T.BID = IT.BID GROUP BY C.CID ORDER BY SUM(TOTAL_COST) DESC")
        response = cursor.fetchall()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to fetch details from database... {str(e)}")
    finally:
        cursor.close()

    return response


@router.get("/stats-3/", tags=["stats-3"])
async def sale_stats_3(begin_date: str, end_date: str, db: mysql.connector.MySQLConnection = Depends(get_db)):
    begin_date = parse(begin_date).strftime("%Y-%m-%d")
    end_date = parse(end_date).strftime("%Y-%m-%d")
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT PID, COUNT(PID) FROM APPEARS_IN WHERE BID IN (SELECT BID FROM TRANSACTION WHERE TDATE > %s AND TDATE < %s) GROUP BY PID ORDER BY COUNT(PID)", (begin_date, end_date))
        response = cursor.fetchall()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to fetch details from database... {str(e)}")
    finally:
        cursor.close()

    return response


@router.get("/stats-4/", tags=["stats-4"])
async def sale_stats_4(begin_date: str, end_date: str, db: mysql.connector.MySQLConnection = Depends(get_db)):
    begin_date = parse(begin_date).strftime("%Y-%m-%d")
    end_date = parse(end_date).strftime("%Y-%m-%d")
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT PID FROM APPEARS_IN WHERE BID IN (SELECT BID FROM TRANSACTION WHERE TDATE > %s AND TDATE < %s GROUP BY CID, BID ORDER BY COUNT(DISTINCT CID) DESC) GROUP BY PID", (begin_date, end_date))
        response = cursor.fetchall()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to fetch details from database... {str(e)}")
    finally:
        cursor.close()

    return response


@router.get("/stats-5/", tags=["stats-5"])
async def sale_stats_5(begin_date: str, end_date: str, db: mysql.connector.MySQLConnection = Depends(get_db)):
    begin_date = parse(begin_date).strftime("%Y-%m-%d")
    end_date = parse(end_date).strftime("%Y-%m-%d")
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT CCNUMBER, T.BID, MAX(TOTAL_COST) FROM TRANSACTION T, (SELECT BID, SUM(QUANTITY*PRICESOLD) AS TOTAL_COST FROM APPEARS_IN GROUP BY BID) IT WHERE T.BID = IT.BID AND TDATE > %s AND TDATE < %s GROUP BY CCNUMBER", (begin_date, end_date))
        response = cursor.fetchall()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to fetch details from database... {str(e)}")
    finally:
        cursor.close()

    return response


@router.get("/stats-6/", tags=["stats-6"])
async def sale_stats_6(begin_date: str, end_date: str, db: mysql.connector.MySQLConnection = Depends(get_db)):
    begin_date = parse(begin_date).strftime("%Y-%m-%d")
    end_date = parse(end_date).strftime("%Y-%m-%d")
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT P.PTYPE, AVG(A.PRICESOLD) FROM APPEARS_IN A JOIN PRODUCT P ON A.PID = P.PID WHERE BID IN (SELECT BID FROM TRANSACTION WHERE TDATE > %s AND TDATE < %s) GROUP BY P.PTYPE", (begin_date, end_date))
        response = cursor.fetchall()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to fetch details from database... {str(e)}")
    finally:
        cursor.close()

    return response


