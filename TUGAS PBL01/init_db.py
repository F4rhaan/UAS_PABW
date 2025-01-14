import sqlite3

def init_db():
    # Connect to SQLite database (creates 'app.db' if it doesn't exist)
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()

    # Check if the 'email' column exists in the 'users' table, and if not, add it
    try:
        cursor.execute("PRAGMA table_info(users);")
        columns = [column[1] for column in cursor.fetchall()]
        if "email" not in columns:
            cursor.execute('''ALTER TABLE users ADD COLUMN email TEXT NOT NULL''')
    except sqlite3.OperationalError:
        # If the 'users' table doesn't exist, recreate it (will remove all data)
        cursor.execute('DROP TABLE IF EXISTS users')

        # Create 'users' table with a 'role' column
        cursor.execute(''' 
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                email TEXT NOT NULL,
                role TEXT DEFAULT 'user'
            )
        ''')

    # Create 'posts' table (if not exists)
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            image_path TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    # Add example users with roles
    cursor.execute(''' 
        INSERT OR IGNORE INTO users (username, password, email, role)
        VALUES
            ('admin', 'admin', 'admin@example.com', 'admin'),
            ('user1', 'user1', 'user1@example.com', 'user'),
            ('user2', 'user2', 'user2@example.com', 'user')
    ''')

    # Add example posts
    cursor.execute(''' 
        INSERT INTO posts (content, image_path, user_id)
        VALUES
            ('This is a text-only post', NULL, 1),
            ('Post with an image', 'images/example_image.jpg', 2)
    ''')

    # Commit changes and close the connection
    conn.commit()
    conn.close()
    print("Database initialized!")

if __name__ == "__main__":
    init_db()
