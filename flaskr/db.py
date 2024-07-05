import sqlite3
from flask import g

DATABASE = 'flaskr/instance/mydatabase.db'

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row  # This allows us to access columns by name.
    return g.db

# @app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    db = get_db()
    curser = db.execute(query, args)
    results = curser.fetchall()
    curser.close()
    if results:
        result = [dict(row) for row in results]
        return (result[0] if one else result)
    else:
        return None if one else []

def execute_db(query, args=(), one=False):
    db = get_db()
    db.execute(query, args)
    db.commit()
    db.close()