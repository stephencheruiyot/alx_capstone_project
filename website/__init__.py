# Import necessary modules and classes
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

# Initialize the SQLAlchemy database instance
db = SQLAlchemy()

# Set the name of the database file
DB_NAME = "database.db"

# Create the Flask application using a factory pattern
def create_app():
    app = Flask(__name__)

    # Configure the application with a secret key and the database URI
    app.config['SECRET_KEY'] = "helloworld"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    # Initialize the database with the Flask application
    db.init_app(app)

    # Import views and auth blueprints
    from .views import views
    from .auth import auth

    # Register the blueprints with the Flask application
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    # Import the User, Post, Comment, and Like models
    from .models import User, Post, Comment, Like

    # Create the database if it doesn't exist
    create_database(app)

    # Initialize the LoginManager for user authentication
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    # Define a user loader function for the LoginManager
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

# Create the database if it doesn't exist
def create_database(app):
    with app.app_context():
        if not path.exists("website/" + DB_NAME):
            db.create_all()
            print("Created database!")
