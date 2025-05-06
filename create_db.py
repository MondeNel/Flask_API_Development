from api import app, db

# Create all database tables
# This script initializes the database by creating tables defined in the SQLAlchemy models.

with app.app_context():  # Ensure we're running within the app context
    # db.create_all() will create all tables defined in the models (UserModel, etc.)
    db.create_all()

    # Confirmation message printed to indicate successful database creation
    print("Database created successfully.")
