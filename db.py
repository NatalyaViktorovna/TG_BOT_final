import os
import psycopg2

def init_db():
    conn = psycopg2.connect(os.environ["DATABASE_URL"])
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id SERIAL PRIMARY KEY,
                user_id BIGINT,
                username TEXT,
                original TEXT,
                translated TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
    conn.commit()
    conn.close()

def log_message_to_db(user_id, username, original, translated):
    conn = psycopg2.connect(os.environ["DATABASE_URL"])
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO messages (user_id, username, original, translated)
            VALUES (%s, %s, %s, %s)
        """, (user_id, username, original, translated))
    conn.commit()
    conn.close()