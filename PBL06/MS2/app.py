from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Database files for DB-A and DB-B
DB_A = "./SiteA/DB-A.db"
DB_B = "./SiteB/DB-B.db"

# Function to connect to a specific database
def get_db_connection(db_name):
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    return conn

# Create user (POST) in DB-A or DB-B
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    db_name = data.get('db_name', "DB-A")  # Default to DB-A if not provided
    name = data.get('name')
    email = data.get('email')

    if db_name not in {"DB-A", "DB-B"}:
        return jsonify({"error": "Invalid 'db_name'. Choose from 'DB-A' or 'DB-B'."}), 400

    if not name or not email:
        return jsonify({"error": "Missing 'name' or 'email' in the request."}), 400

    db_path = DB_A if db_name == "DB-A" else DB_B
    conn = get_db_connection(db_path)
    conn.execute('INSERT INTO users (name, email) VALUES (?, ?)', (name, email))
    conn.commit()
    conn.close()
    
    return jsonify({"message": f"User created successfully in {db_name}"}), 201

# Read users (GET) from DB-A or DB-B
@app.route('/users', methods=['GET'])
def get_users():
    db_name = request.args.get('db_name', "DB-A")  # Default to DB-A if not provided

    if db_name not in {"DB-A", "DB-B"}:
        return jsonify({"error": "Invalid 'db_name'. Choose from 'DB-A' or 'DB-B'."}), 400

    db_path = DB_A if db_name == "DB-A" else DB_B
    conn = get_db_connection(db_path)
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()

    user_list = [{"id": user["id"], "name": user["name"], "email": user["email"]} for user in users]
    return jsonify(user_list)

if __name__ == "__main__":
    app.run(port=5052)  # Running on port 5052
