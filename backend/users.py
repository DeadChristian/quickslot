import sqlite3
import os

DB_PATH = os.path.join("data", "users.db")

def init_user_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            handle TEXT UNIQUE,
            name TEXT,
            email TEXT,
            services TEXT,
            payment_methods TEXT,
            deposit_required INTEGER,
            deposit_amount REAL,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_user(profile):
    init_user_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT OR REPLACE INTO users
        (handle, name, email, services, payment_methods, deposit_required, deposit_amount, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        profile["handle"],
        profile["name"],
        profile["email"],
        ",".join(profile["services"]),
        ",".join(profile["payment_methods"]),
        int(profile["deposit_required"]),
        profile["deposit_amount"],
        profile["created_at"]
    ))
    conn.commit()
    conn.close()

def load_user(handle):
    init_user_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE handle = ?", (handle,))
    row = c.fetchone()
    conn.close()

    if not row:
        return None

    return {
        "id": row[0],
        "handle": row[1],
        "name": row[2],
        "email": row[3],
        "services": row[4].split(","),
        "payment_methods": row[5].split(","),
        "deposit_required": bool(row[6]),
        "deposit_amount": row[7]
    }
