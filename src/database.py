import os
import psycopg2
from dotenv import load_dotenv

def connect_to_bd():
    """
    Connect to the PostgreSQL database.
    """
    
    load_dotenv()

    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )
    conn.set_session(readonly=True) #read-only mode to avoid modifications to the database
    return conn

def query_db(query):
    """
    Execute read-only queries on the PostgreSQL database and return the results.
    """
    if not query.strip().lower().startswith("select"):
        raise ValueError("Only SELECT queries are allowed.")
    
    conn = connect_to_bd()
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    finally:
        cursor.close()
 