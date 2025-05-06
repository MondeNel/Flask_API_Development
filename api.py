from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize the Flask application
app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)

class UserModel(db.Model):
    """
    User model for the database.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'User(name = {self.name}, email = {self.email})'


@app.route('/')
def home():
    """
    Root route of the Flask application.
    @return: HTML welcome message
    """
    return '<h1>Welcome to the Flask API!</h1>'

# Entry point of the application
if __name__ == '__main__':
    app.run(debug=True)
