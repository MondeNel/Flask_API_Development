from flask import Flask

# Initialize the Flask application
app = Flask(__name__)

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
