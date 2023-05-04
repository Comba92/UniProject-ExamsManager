from flask import Flask
from flask_login import LoginManager
from data.models import db

login_manager = LoginManager()


def init_app():
    """Initialize the core application."""

    app = Flask(__name__)
    app.config.from_object('config.DevConfig')

    # Initialize plugins
    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        ## Blueprints ---------------------

        ## DB -----------------------------

        # Check that db is properly initialized
        

        # Else, recreate it all
        print(db.get_engine())
        # db.metadata.drop_all(db.get_engine(), checkfirst=True)
        # db.metadata.create_all(db.get_engine(), checkfirst=True)
        # Insert dummy data
        # Start

    return app
