import sqlite3

conn = sqlite3.connect("iot_attacks.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS attacks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ip TEXT,
    username TEXT,
    password TEXT,
    command TEXT,
    timestamp TEXT
)
""")

conn.commit()
conn.close()

print("Database created successfully")

