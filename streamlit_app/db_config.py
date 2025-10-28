import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Horse1@@",
        database="sportradar_db"
    )
