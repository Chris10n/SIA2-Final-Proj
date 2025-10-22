import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "utilities.db")

def get_connection():
    """Return a connection to the SQLite database."""
    return sqlite3.connect(DB_PATH)
