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
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'User(name = {self.name}, email = {self.email})'


# Request parser for creating users
user_args = reqparse.RequestParser()
user_args.add_argument('name', type=str, help='Name of the user', required=True)
user_args.add_argument('email', type=str, help='Email of the user', required=True)

# Request parser for patching/updating users
patch_args = reqparse.RequestParser()
patch_args.add_argument('name', type=str, help='Updated name of the user')
patch_args.add_argument('email', type=str, help='Updated email of the user')

# Fields for marshalling user data
userFields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String
}


class Users(Resource):
    """
    Resource for handling all users.
    """
    @marshal_with(userFields)
    def get(self):
        """
        Get all users.
        """
        return UserModel.query.all()

    @marshal_with(userFields)
    def post(self):
        """
        Create a new user.
        """
        args = user_args.parse_args()
        if UserModel.query.filter_by(name=args['name']).first():
            abort(400, message="User with this name already exists.")
        new_user = UserModel(name=args['name'], email=args['email'])
        db.session.add(new_user)
        db.session.commit()
        return new_user, 201


class User(Resource):
    """
    Resource for operations on a single user by ID.
    """
    @marshal_with(userFields)
    def get(self, user_id):
        """
        Get a single user by ID.
        """
        user = UserModel.query.get(user_id)
        if not user:
            abort(404, message="User not found.")
        return user

    def delete(self, user_id):
        """
        Delete a user by ID.
        """
        user = UserModel.query.get(user_id)
        if not user:
            abort(404, message="User not found.")
        db.session.delete(user)
        db.session.commit()
        return {'message': f'User {user_id} deleted successfully.'}, 204

    @marshal_with(userFields)
    def patch(self, user_id):
        """
        Partially update a user by ID.
        """
        args = patch_args.parse_args()
        user = UserModel.query.get(user_id)
        if not user:
            abort(404, message="User not found.")

        if args['name']:
            user.name = args['name']
        if args['email']:
            user.email = args['email']

        db.session.commit()
        return user


# Register API routes
api.add_resource(Users, '/api/users')
api.add_resource(User, '/api/users/<int:user_id>')


@app.route('/')
def home():
    """Root route."""
    return '<h1>Welcome to the Flask API!</h1>'


# Run the application
if __name__ == '__main__':
    app.run(debug=True)
