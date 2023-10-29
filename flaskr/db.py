import sqlite3
import hashlib
from flask import g

DATABASE = 'your_database.db'


def connect_db():
    return sqlite3.connect(DATABASE)


def init_db():
    with open('schema.sql', 'r') as f:
        db = get_db()
        db.executescript(f.read())
        db.commit()


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_db()
    return db


def close_db():
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def hash_password(password):
    # Use a stronger password hashing method in a production environment
    return hashlib.md5(password.encode()).hexdigest()
