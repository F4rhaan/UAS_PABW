from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'
UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Database connection helper function
def get_db_connection():
    conn = sqlite3.connect('app.db')
    conn.row_factory = sqlite3.Row
    return conn

# Index route
@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''SELECT posts.content, posts.image_path, posts.timestamp, users.username
                      FROM posts
                      JOIN users ON posts.user_id = users.id
                      ORDER BY posts.timestamp DESC''')
    posts = cursor.fetchall()
    conn.close()

    current_year = datetime.now().year  # Get the current year
    return render_template('index.html', posts=posts, current_year=current_year)

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        # Check if the username already exists
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash("Username already exists. Please choose a different one.", "error")
            return render_template('register.html')

        # Insert the new user into the database
        cursor.execute('INSERT INTO users (username, password, email) VALUES (?, ?, ?)', (username, password, email))
        conn.commit()
        conn.close()

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('login'))
    return render_template('register.html')

# Login route
# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check credentials
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['username'] = user['username']
            session['user_id'] = user['id']
            session['role'] = user['role']
            flash("Login successful!", "success")
            
            # Check if the user is an admin and redirect accordingly
            if user['role'] == 'admin':  # Assuming 'admin' is the role stored in the database
                return redirect(url_for('dashboard'))
            else:
                return redirect(url_for('profile', username=username))
        else:
            flash("Invalid credentials! Please try again.", "error")
    return render_template('login.html')


# Create Post route
@app.route('/create_post', methods=['POST'])
def create_post():
    if 'username' not in session:
        flash("Please log in to create a post!", "error")
        return redirect(url_for('login'))

    content = request.form['content']
    image = request.files['image'] if 'image' in request.files else None
    user_id = session.get('user_id')

    conn = get_db_connection()
    cursor = conn.cursor()

    # Save the uploaded image if it exists
    image_path = None
    if image:
        filename = secure_filename(image.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(image_path)

    # Insert the post into the database
    cursor.execute('INSERT INTO posts (content, image_path, user_id) VALUES (?, ?, ?)', (content, image_path, user_id))
    conn.commit()
    conn.close()

    flash("Post created successfully!", "success")
    return redirect(url_for('profile', username=session['username']))

# Profile route
@app.route('/profile/<username>')
def profile(username):
    # Fetch user data
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, username, email FROM users WHERE username = ?', (username,))
    user_data = cursor.fetchone()
    if not user_data:
        conn.close()
        flash("User not found!", "error")
        return redirect(url_for('index'))

    user_id = user_data['id']

    # Fetch all posts by the user
    cursor.execute('SELECT content, image_path, timestamp FROM posts WHERE user_id = ?', (user_id,))
    posts = cursor.fetchall()
    conn.close()

    # Convert posts to list of dictionaries
    posts = [{"content": post['content'], "image_path": post['image_path'], "timestamp": post['timestamp']} for post in posts]

    return render_template('profile.html', username=username, user_data=user_data, posts=posts)
# Admin dashboard route
# Admin dashboard route
@app.route('/dashboard')
def dashboard():
    if 'role' not in session or session['role'] != 'admin':
        flash("You are not authorized to access the dashboard.", "error")
        return redirect(url_for('index'))

    # Fetch all users
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, username, email FROM users')
    users = cursor.fetchall()

    # Fetch all posts
    cursor.execute('SELECT posts.id, posts.content, posts.timestamp, users.username FROM posts JOIN users ON posts.user_id = users.id')
    posts = cursor.fetchall()
    conn.close()

    return render_template('dashboard.html', users=users, posts=posts)



# Logout route
@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully.", "success")
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
