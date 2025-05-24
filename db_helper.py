import sqlite3

DB_NAME = "data.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            chat_id INTEGER PRIMARY KEY
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS discounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            priceWas REAL,
            priceIs REAL,
            difference REAL,
            discount REAL,
            link TEXT,
            image TEXT
        )
    ''')

    conn.commit()
    conn.close()

def add_user(chat_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (chat_id) VALUES (?)", (chat_id,))
    conn.commit()
    conn.close()

def get_users():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT chat_id FROM users")
    users = [row[0] for row in c.fetchall()]
    conn.close()
    return users

def save_discounts(items):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM discounts")
    for item in items:
        c.execute('''
            INSERT INTO discounts (name, priceWas, priceIs, difference, discount, link, image)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            item.get("name"),
            item.get("priceWas"),
            item.get("priceIs"),
            item.get("difference"),
            item.get("discount"),
            item.get("link"),
            item.get("image"),
        ))
    conn.commit()
    conn.close()

def get_discounts():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT name, link FROM discounts ORDER BY discount DESC")
    discounts = c.fetchall()
    conn.close()
    return discounts
