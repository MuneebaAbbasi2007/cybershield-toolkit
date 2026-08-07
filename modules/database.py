import sqlite3
from datetime import datetime

DB_NAME = "cybershield.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS scan_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tool_name TEXT,
            data TEXT,
            ai_analysis TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_scan(tool_name, data, ai_analysis):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "INSERT INTO scan_history (tool_name, data, ai_analysis, timestamp) VALUES (?, ?, ?, ?)",
        (tool_name, str(data), str(ai_analysis), datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    conn.commit()
    conn.close()

def get_all_scans():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT tool_name, data, ai_analysis, timestamp FROM scan_history ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    results = []
    for row in rows:
        results.append({"tool": row[0], "data": row[1], "ai": row[2], "timestamp": row[3]})
    return results