from utils.utils_api import (
    tx,
    create_connection,
)
from utils.utils_DB import get_table_data

def dbconnect():
    conn = create_connection()
    return conn

def getData():
    conn = dbconnect()
    return get_table_data(conn)
