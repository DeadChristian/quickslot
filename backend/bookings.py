import sqlite3
import os

DB_PATH = os.path.join("data", "bookings.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service TEXT,
            datetime TEXT,
            location TEXT,
            name TEXT,
            email TEXT,
            phone TEXT,
            payment TEXT,
            deposit_required INTEGER,
            deposit_amount REAL,
            status TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_booking(data):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO bookings 
        (service, datetime, location, name, email, phone, payment, deposit_required, deposit_amount, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["service"],
        data["datetime"],
        data["location"],
        data["name"],
        data["email"],
        data["phone"],
        data["payment"],
        int(data["deposit_required"]),
        data["deposit_amount"],
        data["status"],
        data["created_at"]
    ))
    conn.commit()
    conn.close()
