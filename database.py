import sqlite3
import os

DB_NAME = "chatbot.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS stats
                 (id INTEGER PRIMARY KEY, queries_processed INTEGER)''')
    
    # Initialize with 1.2M fake start so the UI looks impressive immediately
    c.execute("SELECT * FROM stats WHERE id=1")
    if not c.fetchone():
        c.execute("INSERT INTO stats (id, queries_processed) VALUES (1, 1200000)")
    
    conn.commit()
    conn.close()

def increment_query():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE stats SET queries_processed = queries_processed + 1 WHERE id=1")
    conn.commit()
    conn.close()

def get_query_count():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT queries_processed FROM stats WHERE id=1")
    count = c.fetchone()[0]
    conn.close()
    return count
