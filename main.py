from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse, fields, marshal_with, abort

# Initialize the Flask application
app = Flask(__name__)

# Configure the SQLite database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

# Initialize SQLAlchemy with the Flask app
db = SQLAlchemy(app)

# Initialize Flask-Restful API
api = Api(app)


class UserModel(db.Model):
    """
    SQLAlchemy model representing a User entity in the database.
    Fields:
        - id (Integer): Primary key
        - name (String): Unique username (required)
        - email (String): Unique email address (required)
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'User(name = {self.name}, email = {self.email})'


# Request parser to handle and validate incoming POST request data
user_args = reqparse.RequestParser()
user_args.add_argument('name', type=str, help='Name of the user', required=True)
user_args.add_argument('email', type=str, help='Email of the user', required=True)

# Define the fields for marshalling user data in API responses
userFields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String
}


class Users(Resource):
    """
    Resource for handling user-related API operations.
    Supports:
        - GET: Retrieve all users
        - POST: Create a new user
    """
    @marshal_with(userFields)
    def get(self):
        """
        Retrieve and return all users in the database.

        Returns:
            List of users serialized in JSON format.
        """
        users = UserModel.query.all()
        return users

    @marshal_with(userFields)
    def post(self):
        """
        Create and store a new user in the database.

        Returns:
            JSON of the created user with HTTP 201 status code.

        Raises:
            400 Bad Request if a user with the same name already exists.
        """
        args = user_args.parse_args()
        user = UserModel(name=args['name'], email=args['email'])

        # Check for existing user with the same name
        existing_user = UserModel.query.filter_by(name=args['name']).first()
        if existing_user:
            abort(400, message="User with this name already exists.")

        # Add and commit the new user to the database
        db.session.add(user)
        db.session.commit()
        return user, 201



class User(Resource):
    """
    Resource for operations on a single user.
    Supports:
        - DELETE: Delete a user by ID
    """
    def delete(self, user_id):
        """
        Delete a user by their ID.

        Args:
            user_id (int): ID of the user to delete

        Returns:
            A success message with HTTP 204 status code

        Raises:
            404 Not Found if the user does not exist
        """
        user = UserModel.query.get(user_id)
        if not user:
            abort(404, message=f"User with ID {user_id} not found.")

        db.session.delete(user)
        db.session.commit()
        return {"message": f"User with ID {user_id} has been deleted."}, 204

# Register the Users resource to the '/api/users' endpoint
api.add_resource(Users, '/api/users')


@app.route('/')
def home():
    """
    Root route of the Flask application.

    Returns:
        A simple HTML welcome message.
    """
    return '<h1>Welcome to the Flask API!</h1>'


# Entry point of the application
if __name__ == '__main__':
    app.run(debug=True)
