import sqlite3
import os

def init_db(db_name, dummy_data):
    # Ensure the directory exists
    os.makedirs(os.path.dirname(db_name), exist_ok=True)

    # Create or connect to the SQLite database
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    # Create table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT
    )''')

    # Insert dummy data
    cursor.executemany("INSERT INTO users (name, email) VALUES (?, ?)", dummy_data)
    
    connection.commit()
    connection.close()

if __name__ == "__main__":
    # Dummy data for DB-A and DB-B
    dummy_data_a = [
        ('John Doe', 'john@example.com'),
        ('Jane Smith', 'jane@example.com'),
        ('Mike Johnson', 'mike@example.com')
    ]
    dummy_data_b = [
        ('Alice Brown', 'alice@example.com'),
        ('Bob White', 'bob@example.com'),
        ('Charlie Green', 'charlie@example.com')
    ]

    # Initialize DB-A and DB-B with dummy data
    init_db('./SiteA/DB-A.db', dummy_data_a)
    init_db('./SiteB/DB-B.db', dummy_data_b)

    print("Databases and dummy data created successfully!")
