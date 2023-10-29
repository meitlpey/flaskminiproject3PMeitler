import sqlite3
import hashlib  # Use a stronger hashing method in production

DATABASE = 'your_database.db'

def get_db():
    db = sqlite3.connect(DATABASE)
    return db

def init_db():
    with open('schema.sql', 'r') as f:
        db = get_db()
        db.executescript(f.read())
        db.commit()

def close_db():
    db = get_db()
    db.close()

def register_user(username, password):
    db = get_db()
    password = hashlib.md5(password.encode()).hexdigest()  # Use a stronger hashing method in production
    db.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    db.commit()

def get_user_by_id(user_id):
    db = get_db()
    cursor = db.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    return user

def get_user_by_username(username):
    db = get_db()
    cursor = db.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    return user

def create_poll(title, options, admin_id):
    db = get_db()
    db.execute("INSERT INTO polls (title, options, admin_id) VALUES (?, ?, ?)", (title, options, admin_id))
    db.commit()

# Add more database functions for your specific application needs
