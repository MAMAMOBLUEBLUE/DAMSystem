# db.py
import pymysql

def get_db_conn():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='qrdatabase',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor  # <--- important
    )
    return conn

