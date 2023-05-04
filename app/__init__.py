from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from data.models import db
from data.startup import insert_dummy_data

login_manager = LoginManager()


def init_app():
    """Initialize the core application."""

    app = Flask(__name__)
    app.config.from_object('config.DevConfig')

    # Initialize plugins
    db.init_app(app)
    login_manager.init_app(app)
    Bcrypt(app)

    with app.app_context():
        ## Blueprints ---------------------

        ## DB -----------------------------

        # Check that db is properly initialized
        

        # Else, recreate it all
        # db.metadata.drop_all(db.get_engine())
        # db.metadata.create_all(db.get_engine())
        insert_dummy_data(db)
        # Start

    return app
