import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "user": "e_commerce",
    "password": "password",
    "database": "e_commerce"
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)
