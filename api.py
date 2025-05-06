from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse, fields, marshal_with, abort

# Initialize the Flask application
app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)

# Initialize Flask-Restful API
api = Api(app)

class UserModel(db.Model):
    """
    User model for the database.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'User(name = {self.name}, email = {self.email})'



user_args = reqparse.RequestParser()
user_args.add_argument('name', type=str, help='Name of the user', required=True)
user_args.add_argument('email', type=str, help='Email of the user', required=True)


# serialization format for the user model
# This is used to define how the user data will be represented in the API response.
userFields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String
}

# Define the User resource for handling user-related operations
class Users(Resource):
    """
    Resource for handling user-related operations.
    """
    @marshal_with(userFields)
    def get(self):
        """
        Get all users from the database.
        @return: List of users in JSON format
        """
        users = UserModel.query.all()
        return users
    
    @marshal_with(userFields)
    def post(self):
        """
        Create a new user in the database.
        @return: Created user in JSON format
        """
        args = user_args.parse_args()
        user = UserModel(name=args['name'], email=args['email'])
        
        # Check if the user already exists
        existing_user = UserModel.query.filter_by(name=args['name']).first()
        if existing_user:
            abort(400, message="User with this name already exists.")
        
        db.session.add(user)
        db.session.commit()
        return user, 201

api.add_resource(Users, '/api/users')
  


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
