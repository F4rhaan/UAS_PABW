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

# Create user (POST) in DB-B first, then in DB-A
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')

    if not name or not email:
        return jsonify({"error": "Missing 'name' or 'email' in the request."}), 400

    # Save to DB-B first
    conn_b = get_db_connection(DB_B)
    conn_b.execute('INSERT INTO users (name, email) VALUES (?, ?)', (name, email))
    conn_b.commit()
    conn_b.close()

    # Save to DB-A
    conn_a = get_db_connection(DB_A)
    conn_a.execute('INSERT INTO users (name, email) VALUES (?, ?)', (name, email))
    conn_a.commit()
    conn_a.close()

    return jsonify({"message": "User created successfully in DB-B and DB-A"}), 201

# Read users (GET) from DB-A or DB-B
@app.route('/users', methods=['GET'])
def get_users():
    db_name = request.args.get('db_name')  # Specify the target database as a query parameter

    if db_name not in {"DB-A", "DB-B"}:
        return jsonify({"error": "Invalid 'db_name'. Choose from 'DB-A' or 'DB-B'."}), 400

    db_path = DB_A if db_name == "DB-A" else DB_B
    conn = get_db_connection(db_path)
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()

    user_list = [{"id": user["id"], "name": user["name"], "email": user["email"]} for user in users]
    return jsonify(user_list)

if __name__ == "__main__":
    app.run(port=5053)  # Running on port 5053
