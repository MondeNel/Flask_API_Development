from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse, fields, marshal_with, abort
import csv
import os

# Initialize the Flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
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


# Create CSV export function
def export_users_to_csv():
    users = UserModel.query.all()
    file_path = os.path.join(os.getcwd(), 'users.csv')

    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'Name', 'Email'])  # Header
        for user in users:
            writer.writerow([user.id, user.name, user.email])


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
        return UserModel.query.all()

    @marshal_with(userFields)
    def post(self):
        args = user_args.parse_args()
        if UserModel.query.filter_by(name=args['name']).first():
            abort(400, message="User with this name already exists.")
        new_user = UserModel(name=args['name'], email=args['email'])
        db.session.add(new_user)
        db.session.commit()
        export_users_to_csv()
        return new_user, 201


class User(Resource):
    """
    Resource for operations on a single user by ID.
    """
    @marshal_with(userFields)
    def get(self, user_id):
        user = UserModel.query.get(user_id)
        if not user:
            abort(404, message="User not found.")
        return user

    def delete(self, user_id):
        user = UserModel.query.get(user_id)
        if not user:
            abort(404, message="User not found.")
        
        db.session.delete(user)
        db.session.commit()
        export_users_to_csv()

        # Get remaining users
        remaining_users = UserModel.query.all()
        return {
            'message': f'User {user_id} deleted successfully.',
            'remaining_users': [{'id': u.id, 'name': u.name, 'email': u.email} for u in remaining_users]
        }, 200

    @marshal_with(userFields)
    def patch(self, user_id):
        args = patch_args.parse_args()
        user = UserModel.query.get(user_id)
        if not user:
            abort(404, message="User not found.")

        if args['name']:
            user.name = args['name']
        if args['email']:
            user.email = args['email']

        db.session.commit()
        export_users_to_csv()
        return user


# Register API routes
api.add_resource(Users, '/api/users')
api.add_resource(User, '/api/users/<int:user_id>')


@app.route('/')
def home():
    return '<h1>Welcome to the Flask API!</h1>'


# Run the application
if __name__ == '__main__':
    # Ensure DB is created and CSV file exists on first run
    with app.app_context():
        db.create_all()
        export_users_to_csv()

    app.run(debug=True)
