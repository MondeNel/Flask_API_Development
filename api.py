from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse, fields, marshal_with, abort

# Initialize the Flask application
app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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


# Fields for marshaling the response data
user_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String
}

class UserResource(Resource):
    """
    User resource for handling CRUD operations via Flask-RESTful.
    """

    # Set up request parser to validate incoming data
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help="Name cannot be blank")
    parser.add_argument('email', type=str, required=True, help="Email cannot be blank")

    def get(self, user_id):
        """
        Get a single user by ID
        """
        user = UserModel.query.get(user_id)
        if not user:
            abort(404, message="User not found")
        return marshal_with(user, user_fields)

    def post(self):
        """
        Create a new user
        """
        args = self.parser.parse_args()
        new_user = UserModel(name=args['name'], email=args['email'])
        db.session.add(new_user)
        db.session.commit()
        return marshal_with(new_user, user_fields), 201

    def put(self, user_id):
        """
        Update an existing user
        """
        user = UserModel.query.get(user_id)
        if not user:
            abort(404, message="User not found")
        
        args = self.parser.parse_args()
        user.name = args['name']
        user.email = args['email']
        db.session.commit()
        return marshal_with(user, user_fields)

    def delete(self, user_id):
        """
        Delete a user by ID
        """
        user = UserModel.query.get(user_id)
        if not user:
            abort(404, message="User not found")
        
        db.session.delete(user)
        db.session.commit()
        return '', 204


class UserListResource(Resource):
    """
    Resource for handling user collection.
    """

    def get(self):
        """
        Get all users
        """
        users = UserModel.query.all()
        return [marshal_with(user, user_fields) for user in users]

    def post(self):
        """
        Create a new user
        """
        args = UserResource.parser.parse_args()
        new_user = UserModel(name=args['name'], email=args['email'])
        db.session.add(new_user)
        db.session.commit()
        return marshal_with(new_user, user_fields), 201


@app.route('/')
def home():
    """
    Root route of the Flask application.
    @return: HTML welcome message
    """
    return '<h1>Welcome to the Flask API!</h1>'

# Add the API resources to the Flask app
api.add_resource(UserListResource, '/users')
api.add_resource(UserResource, '/users/<int:user_id>')

# Entry point of the application
if __name__ == '__main__':
    # Create the database tables
    with app.app_context():
        db.create_all()

    app.run(debug=True)
