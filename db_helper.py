import sqlite3
from contextlib import closing

DB_PATH = 'discounts.db'

def init_db():
    with closing(sqlite3.connect(DB_PATH)) as conn:
        with conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS discounts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    link TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY
                )
            ''')

def add_user(user_id):
    with closing(sqlite3.connect(DB_PATH)) as conn:
        with conn:
            conn.execute('INSERT OR IGNORE INTO users (user_id) VALUES (?)', (user_id,))

def save_discount(title, link):
    with closing(sqlite3.connect(DB_PATH)) as conn:
        with conn:
            conn.execute('INSERT INTO discounts (title, link) VALUES (?, ?)', (title, link))

def get_discounts():
    with closing(sqlite3.connect(DB_PATH)) as conn:
        cur = conn.execute('SELECT title, link FROM discounts ORDER BY timestamp DESC')
        return cur.fetchall()

def get_users():
    with closing(sqlite3.connect(DB_PATH)) as conn:
        cur = conn.execute('SELECT user_id FROM users')
        return [row[0] for row in cur.fetchall()]
