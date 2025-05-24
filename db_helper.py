import sqlite3
import logging

DB_FILE = "users.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS discounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price_was REAL,
            price_is REAL,
            discount INTEGER,
            link TEXT,
            image TEXT
        )
    ''')
    conn.commit()
    conn.close()

def get_top_discounts(min_discount=30):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT name, discount, link FROM discounts WHERE discount >= ? ORDER BY discount DESC", (min_discount,))
    results = c.fetchall()
    conn.close()
    return results