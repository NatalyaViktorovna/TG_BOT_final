import sqlite3

def init_db():
    conn = sqlite3.connect("messages.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            username TEXT,
            original TEXT,
            translated TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def log_message_to_db(user_id, username, original, translated):
    conn = sqlite3.connect("messages.db")
    c = conn.cursor()
    c.execute("""
        INSERT INTO messages (user_id, username, original, translated)
        VALUES (?, ?, ?, ?)
    """, (user_id, username, original, translated))
    conn.commit()
    conn.close()
