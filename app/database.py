import sqlite3

connection = sqlite3.connect("database.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS shipments (
        id INTEGER,
        weight REAL,
        content TEXT,
        destination INTEGER,
        status TEXT
    )
""")

connection.close()