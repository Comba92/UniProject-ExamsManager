from flask import Flask
from data.models import db
from data.startup import insert_dummy_data


login_manager = LoginManager()


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

        # Create Database Models

        db.metadata.drop_all(db.get_engine())
        db.metadata.create_all(db.get_engine())
        insert_dummy_data(db)
        
    return app
