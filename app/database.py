import mysql.connector
from .config import config


# Connect to server
DB_CONFIG = {
    "host": config.DB_HOST,
    "user": config.DB_USER,
    "password": config.DB_PASSWORD,
    "database": config.DB_DATABASE,
}

def get_db():
    db = mysql.connector.connect(**DB_CONFIG)
    try:
        yield db
    finally:
        db.close()


