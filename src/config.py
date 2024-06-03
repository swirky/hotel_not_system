from flask import Flask, g
import sqlite3

app=Flask(__name__)
app.config['SECRET_KEY'] = '123GoniszTy!' 
app_info={'db_file': r"database\base.db"}

def get_db():
    """
    The get_db function above is a helper function. It opens a new database connection if there is none yet for the current application context.
    It also binds the sqlite3.Row object to each row, so that you can access columns by name instead of by index.
    
    :return: A connection to the database
    :doc-author: Trelent
    """
    if not hasattr(g, 'sqlite_db'):
        conn=sqlite3.connect(app_info['db_file'])
        conn.row_factory=sqlite3.Row
        g.sqlite_db= conn
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """
    The close_db function is a teardown function that will be called after each request. 
    It checks if the application has an attribute named sqlite_db, and if it does, closes the database connection.
    
    :param error: Pass in the error message to be displayed on the page
    :return: Nothing
    :doc-author: Trelent
    """
    if hasattr(g,'sqlite_db'):
        g.sqlite_db.close()