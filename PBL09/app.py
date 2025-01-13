from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request, session, flash
from itsdangerous import URLSafeSerializer
from forms import LoginForm, PostForm, RegisterForm  # Import the RegisterForm
from extensions import db
from models import User, Post
from logging_config import setup_logging, log_action  # Import log_action

# Set up the custom logging
setup_logging()

app = Flask(__name__)

app.secret_key = 'Kulkas_LG_2-Pintu_Minat_Inbox'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

# Initialize SQLAlchemy
db.init_app(app)  # Initialize db with the Flask app

# Serializer for encrypting links
serializer = URLSafeSerializer(app.secret_key)

@app.route('/dashboard')
def dashboard():
    """
    Dashboard for admin users.
    Unauthorized users are redirected to the home page.
    """
    if 'user_id' not in session:
        flash("You must be logged in to access the dashboard.", "danger")
        log_action("Unauthorized access attempt to the dashboard", request)  # Pass request here
        return redirect(url_for('login'))

    # Get the current user
    user = User.query.get(session['user_id'])
    if user and user.role == 'admin':  # Only admin users can access the dashboard
        log_action(f"Admin {user.username} accessed the dashboard.", request)  # Pass request here
        
        # Get the most recent posts
        posts = Post.query.order_by(Post.timestamp.desc()).limit(5).all()  # You can adjust the limit

        return render_template('dashboard.html', user=user, posts=posts)
    else:
        flash("You are not authorized to access this page.", "danger")
        log_action(f"Unauthorized access attempt to the dashboard by user {user.username if user else 'Unknown'}", request)  # Pass request here
        return redirect(url_for('home'))

@app.route('/logs')
def logs():
    """
    Show the recent logs for admin users.
    Unauthorized users are redirected to the home page.
    """
    if 'user_id' not in session:
        flash("You must be logged in to access the logs page.", "danger")
        log_action("Unauthorized access attempt to the logs page", request)  # Pass request here
        return redirect(url_for('login'))

    # Get the current user
    user = User.query.get(session['user_id'])
    if user and user.role == 'admin':  # Only admin users can access the logs
        log_action(f"Admin {user.username} accessed the logs page.", request)  # Pass request here
        
        # Read recent logs from the log file
        try:
            with open('logs/app_actions.log', 'r') as log_file:
                logs = log_file.readlines()[-20:]  # Get the last 20 lines of the log file
        except FileNotFoundError:
            logs = ["Log file not found."]

        return render_template('logs.html', logs=logs)
    else:
        flash("You are not authorized to access this page.", "danger")
        log_action(f"Unauthorized access attempt to the logs page by user {user.username if user else 'Unknown'}", request)  # Pass request here
        return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        # Check if user already exists
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already taken.', 'danger')
            log_action(f'Failed registration attempt: {username} already exists.', request)  # Pass request here
        else:
            # Create new user with hashed password
            new_user = User(username=username, role='user')  # Default role is 'user'
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully! You can now log in.', 'success')
            log_action(f'User {username} registered successfully.', request)  # Pass request here
            return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/')
def home():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    current_user = User.query.get(session.get('user_id'))
    log_action('Home page accessed.', request)  # Pass request here
    return render_template('home.html', posts=posts, serializer=serializer, user=current_user)

@app.route('/profile/<encrypted_id>')
def profile(encrypted_id):
    try:
        user_id = serializer.loads(encrypted_id)  # Decrypt ID
        user = User.query.get(user_id)
        if user:
            log_action(f'Profile page accessed for user {user.username}.', request)  # Pass request here
            return render_template('profile.html', user=user)
    except Exception as e:
        flash("Invalid profile link!", "danger")
        log_action(f'Failed to access profile: {e}', request)  # Pass request here
    return redirect(url_for('home'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):  # Use check_password method
            session['user_id'] = user.id
            flash('Logged in successfully.', 'success')
            log_action(f'User {user.username} logged in successfully.', request)  # Pass request here
            return redirect(url_for('home'))
        flash('Invalid username or password.', 'danger')
        log_action(f'Failed login attempt for username: {form.username.data}', request)  # Pass request here
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully.', 'success')
    log_action(f'User logged out successfully.', request)  # Pass request here
    return redirect(url_for('home'))

@app.route('/post', methods=['GET', 'POST'])
def post():
    if 'user_id' not in session:
        flash('Please login to create a post.', 'danger')
        log_action('Guest user tried to create a post without logging in.', request)  # Pass request here
        return redirect(url_for('login'))

    form = PostForm()
    if form.validate_on_submit():
        new_post = Post(
            content=form.content.data,
            timestamp=datetime.now(),
            user_id=session['user_id']
        )
        db.session.add(new_post)
        db.session.commit()
        flash('Post created successfully!', 'success')
        log_action(f'New post created by user {session["user_id"]}.', request)  # Pass request here
        return redirect(url_for('home'))
    return render_template('post.html', form=form)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Creates all tables
    app.run(debug=True)
