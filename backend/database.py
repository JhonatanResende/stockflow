import psycopg2
from dotenv import load_dotenv
import os

load_dotenv(encoding='utf-8')

def get_connection():
    connection = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        dbname=os.getenv("DB_NAME"),
        port=os.getenv("DB_PORT")
    )
    return connection