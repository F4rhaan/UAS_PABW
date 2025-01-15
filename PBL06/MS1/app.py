from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Database file for DB-A
DB_A = "./SiteA/DB-A.db"

# Function to connect to DB-A
def get_db_connection():
    conn = sqlite3.connect(DB_A)
    conn.row_factory = sqlite3.Row
    return conn

# Create user (POST) in DB-A
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')

    if not name or not email:
        return jsonify({"error": "Missing 'name' or 'email' in the request."}), 400

    conn = get_db_connection()
    conn.execute('INSERT INTO users (name, email) VALUES (?, ?)', (name, email))
    conn.commit()
    conn.close()
    
    return jsonify({"message": "User created successfully in DB-A"}), 201

# Read users (GET) from DB-A
@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()

    user_list = [{"id": user["id"], "name": user["name"], "email": user["email"]} for user in users]
    return jsonify(user_list)

if __name__ == "__main__":
    app.run(port=5051)  # Running on port 5051
