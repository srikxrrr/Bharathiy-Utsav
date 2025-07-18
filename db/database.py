import sqlite3

def get_connection():
    conn = sqlite3.connect("bharatiy_utsav.db", check_same_thread=False)
    return conn

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # User table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # Festival uploads table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS festivals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT,
            description TEXT,
            category TEXT,
            latitude REAL,
            longitude REAL,
            filename TEXT,
            filetype TEXT,
            upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    conn.commit()
    conn.close()
