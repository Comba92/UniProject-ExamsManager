"""
Module for dummy data generation

"""

from flask import Flask
from data.models import db
from flask_login import LoginManager
from data.database import create_db

# Constructors
login_manager = LoginManager()


# App Initializer
def init_app():
    """
    Initialize the core application.

    """
    # Application Configuration
    app = Flask(__name__)
    app.config.from_object('config.DevConfig')

    # Initialize Plugins
    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        # Register Blueprints

        # # Setup Flask-User and specify the User data-model
        # user_manager = UserManager(app, db, User)

        # Create Database Models
        # create_db(engine=db, drop_first=True)
        # Create all database tables
        db.drop_all()
        db.create_all()
        # Create roles
        # TODO: FIX, the roles are not accepted by SupaBase, only by a local postgres
        # init_serverside_roles(session=db.session, drop_first=False)
        # Insert Dummy Data
        # insert_dummy_data(db, drop_first=True)

    return app
