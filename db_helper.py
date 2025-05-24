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

def save_discounts(items):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM discounts")  # پاک کردن داده‌های قبلی
    for item in items:
        c.execute('''
            INSERT INTO discounts (name, price_was, price_is, discount, link, image)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (item["name"], item["priceWas"], item["priceIs"], item["discount"], item["link"], item["image"]))
    conn.commit()
    conn.close()

def get_top_discounts(min_discount=30):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT name, discount, link FROM discounts WHERE discount >= ? ORDER BY discount DESC", (min_discount,))
    results = c.fetchall()
    conn.close()
    return results
