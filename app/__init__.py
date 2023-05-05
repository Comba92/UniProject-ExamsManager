from flask import Flask
from data.models import db
from flask_login import LoginManager
from data.startup import insert_dummy_data
from data.roles import init_serverside_roles

login_manager = LoginManager()


def create_db(engine, drop_first=True):
    """
    Creates tables if the engine has the privilege to do so

    :param engine:
    :param drop_first:
    :return:
    """
    if drop_first:
        engine.metadata.drop_all(engine.get_engine())
    engine.metadata.create_all(engine.get_engine())
    pass


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
        create_db(engine=db, drop_first=False)
        # Create roles
        # TODO: FIX, the roles are not accepted by SupaBase, only by a local postgres
        # init_serverside_roles(session=db.session, drop_first=False)
        # Insert Dummy Data
        # insert_dummy_data(db)

    return app
