import sqlite3

conn = sqlite3.connect("roulette.db")

cur = conn.cursor()

# جدول الروليتات
cur.execute('''
CREATE TABLE IF NOT EXISTS roulettes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    max_users INTEGER,
    winners INTEGER,
    channel TEXT,
    creator INTEGER,
    type TEXT
)
''')

# جدول المشاركين
cur.execute('''
CREATE TABLE IF NOT EXISTS participants(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    roulette_id INTEGER,
    user_id INTEGER
)
''')

conn.commit()
