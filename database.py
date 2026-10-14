import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'jobs.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company TEXT,
        role TEXT,
        status TEXT,
        match_score INTEGER,
        date_applied TEXT
    )''')
    conn.commit()
    conn.close()
    print("Database ready! jobs.db created")

def save_application(data):
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''INSERT INTO applications 
        (company, role, status, match_score, date_applied)
        VALUES (?, ?, ?, ?, ?)''',
        (data.get('company'), data.get('role'), 
         data.get('status', 'Applied'), data.get('match_score', 0), 
         data.get('date', datetime.now().strftime('%Y-%m-%d'))))
    conn.commit()
    conn.close()

def get_all_applications():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.execute('SELECT * FROM applications ORDER BY id DESC')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

if __name__ == '__main__':
    init_db()