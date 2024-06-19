import mysql.connector
from flask import g

HOST = 'localhost'
USER = 'dbs'
PASSWORD = 'password'
DATABASE = 'WDIS'


def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE,
            autocommit=True
        )
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()