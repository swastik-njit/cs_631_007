import os
from dotenv import load_dotenv


load_dotenv()

class Config:
    PROJECT_NAME: str = "Newark-IT"
    PROJECT_VERSION: str = "1.0.0"
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", 3306)
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_DATABASE: str = os.getenv("DB_DATABASE", "testcase")

config = Config()


