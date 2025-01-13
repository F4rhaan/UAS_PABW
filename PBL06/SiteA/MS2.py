from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Function to connect to a specific database
def get_db_connection(db_name):
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row  # Enable row access
    return conn

# Map database names to file paths
DATABASES = {
    "DB-A": "./SiteA/DB-A.db",
    "DB-B": "./SiteB/DB-B.db"
}

# Create user (POST) with dynamic database selection
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    db_name = data.get('db_name')  # Specify the target database in the request
    name = data.get('name')
    email = data.get('email')

    if not db_name or db_name not in DATABASES:
        return jsonify({"error": "Invalid or missing 'db_name'. Choose from 'DB-A' or 'DB-B'."}), 400
    
    if not name or not email:
        return jsonify({"error": "Missing 'name' or 'email' in the request."}), 400

    conn = get_db_connection(DATABASES[db_name])
    conn.execute('INSERT INTO users (name, email) VALUES (?, ?)', (name, email))
    conn.commit()
    conn.close()
    
    return jsonify({"message": f"User created successfully in {db_name}"}), 201

# Read users (GET) with dynamic database selection
@app.route('/users', methods=['GET'])
def get_users():
    db_name = request.args.get('db_name')  # Specify the target database as a query parameter

    if not db_name or db_name not in DATABASES:
        return jsonify({"error": "Invalid or missing 'db_name'. Choose from 'DB-A' or 'DB-B'."}), 400

    conn = get_db_connection(DATABASES[db_name])
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    
    user_list = [{"id": user["id"], "name": user["name"], "email": user["email"]} for user in users]
    
    return jsonify(user_list)

# Update user (PUT) with dynamic database selection
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    db_name = data.get('db_name')  # Specify the target database in the request
    name = data.get('name')
    email = data.get('email')

    if not db_name or db_name not in DATABASES:
        return jsonify({"error": "Invalid or missing 'db_name'. Choose from 'DB-A' or 'DB-B'."}), 400

    if not name or not email:
        return jsonify({"error": "Missing 'name' or 'email' in the request."}), 400

    conn = get_db_connection(DATABASES[db_name])
    conn.execute('UPDATE users SET name = ?, email = ? WHERE id = ?', (name, email, id))
    conn.commit()
    conn.close()
    
    return jsonify({"message": f"User updated successfully in {db_name}"}), 200

# Delete user (DELETE) with dynamic database selection
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    db_name = request.args.get('db_name')  # Specify the target database as a query parameter

    if not db_name or db_name not in DATABASES:
        return jsonify({"error": "Invalid or missing 'db_name'. Choose from 'DB-A' or 'DB-B'."}), 400

    conn = get_db_connection(DATABASES[db_name])
    conn.execute('DELETE FROM users WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    return jsonify({"message": f"User deleted successfully from {db_name}"}), 200

if __name__ == "__main__":
    app.run(port=5052)  # Running on port 5052
