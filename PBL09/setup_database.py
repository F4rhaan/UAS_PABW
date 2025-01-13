from app import app, db  # Import the app and db objects from your Flask app module
from models import User

def recreate_database():
    """
    Drops all tables and recreates the database schema.
    """
    print("Recreating database...")
    with app.app_context():  # Use app context to access db operations
        db.drop_all()
        db.create_all()
    print("Database recreated successfully!")

def add_sample_data():
    """
    Adds sample data (e.g., users) to the database.
    """
    print("Adding sample data...")
    with app.app_context():  # Use app context to access db operations
        # Add an admin user
        admin = User(username='admin', role='admin')
        admin.set_password('admin')  # Hash the password

        # Add a regular user
        user = User(username='user', role='user')
        user.set_password('user')  # Hash the password

        # Commit the users to the database
        db.session.add(admin)
        db.session.add(user)
        db.session.commit()

    print("Sample data added successfully!")

if __name__ == "__main__":
    recreate_database()
    add_sample_data()
