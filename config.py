"""Set Flask and SqlAlchemy configuration variables"""
from os import environ, path
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from sqlalchemy import engine_from_config
from sqlalchemy.pool import QueuePool
from sqlalchemy.engine import URL

PRIVILEGES = ["SELECT", "INSERT", "UPDATE", "DELETE", "ALL"]

ENG_PROD_CONFIG = {
    'sqlalchemy.url': "",
    'sqlalchemy.hide_parameters': True,
    'sqlalchemy.pool_use_lifo': False,
    'sqlalchemy.pool_size': 20,
    'sqlalchemy.max_overflow': 0,
}

ENG_DEV_CONFIG = {
    'sqlalchemy.url': "",
    'sqlalchemy.echo': True,
    'sqlalchemy.echo_pool': True,
    'sqlalchemy.poolclass': QueuePool,
    'sqlalchemy.pool_use_lifo': True,
    'sqlalchemy.pool_pre_ping': True,
    'sqlalchemy.pool_size': 10,
    'sqlalchemy.max_overflow': 5,
}


def get_from_env(env_var: str):
    """
    Simple util function for loading global variables from .env file in root directory

    :param env_var: a string containing a variable name from .env
    :return: the global variable requested, if present
    :raises: Exception: if env_var is not a string or if it is not present in the .env file
    """
    if isinstance(env_var, str):
        # Finds the path of config.py
        # This file should be in the root directory
        basedir = path.abspath(path.dirname(__file__))
        # Finds .env file in root directory of the project
        load_dotenv(path.join(basedir, '.env'))
        return environ.get(env_var)
    else:
        raise TypeError("Requested str type for env_var")
    pass


# There must be at least one valid user for the database, the superuser
VALID_USERS = {
    # "postgres"
    get_from_env("USER"): get_from_env("PASSWORD"),
    # "board"
    get_from_env("BOARD"): generate_password_hash(password=get_from_env("BOARD_PSW"), salt_length=8),
    # "professor"
    get_from_env("PROF"): generate_password_hash(password=get_from_env("PROF_PSW"), salt_length=8),
    # "student"
    get_from_env("STUD"): generate_password_hash(password=get_from_env("STUD_PSW"), salt_length=8),
    # "admin"
    get_from_env("ADMIN"): generate_password_hash(password=get_from_env("ADMIN_PSW"), salt_length=8),
}


def add_valid_user(user: str, password: str):
    """
    Adds user to global VALID_USERS if the information is found in the .env file

    :param user: str representing the name of the global variable associated with the database name for a role
    :param password: str representing the name of the global variable associated with the database password for a role
    :return: None
    """
    if VALID_USERS is not None and isinstance(VALID_USERS, dict):
        user_str = get_from_env(user)
        password_str = get_from_env(password)
        if len(user_str) >= 4 and len(password_str) >= 8:
            VALID_USERS.update({user_str: password_str})
    pass


class EngineFactory:
    """
    Engine configuration for user-specific connections. The parameters of the engine configuration
    are specified in the config.py file
    """
    __url = None

    def __init__(self, user):
        """
        Constructor for EngineFactory object
        :param user: must be one of the following "postgres", "listener", "premium", "creator", "admin"
        :raises Ex
        """

        if user in VALID_USERS:
            self.__set_url(user, password=VALID_USERS[user])
        else:
            raise EnvironmentError("ROLE: " + user + " is not defined in local database")
        pass

    def __set_url(self, user, password, pooling=False):
        if pooling:
            self.__url = URL.create(
                drivername=get_from_env("DRIVER"),
                username=user,
                password=password,
                host=get_from_env("HOST"),
                port=get_from_env("PORT_POOLING"),
                database=get_from_env("DATABASE")
            )
        else:
            self.__url = URL.create(
                drivername=get_from_env("DRIVER"),
                username=user,
                password=password,
                host=get_from_env("HOST"),
                port=get_from_env("PORT_DIRECT"),
                database=get_from_env("DATABASE")
            )
        pass

    def get_url(self):
        """
        Returns the url connection string for this instance of the EngineFactory
        :return: url as str type
        """
        return self.__url.render_as_string(hide_password=False)

    def get_engine(self, debug=True):
        """
        Returns the ROLE-specific engine for database operations
        :return: Engine for local database instance
        """
        if self.__url is None:
            raise AttributeError("EngineFactory not initialized")
        else:
            ENG_DEV_CONFIG["sqlalchemy.url"] = self.__url
            ENG_PROD_CONFIG["sqlalchemy.url"] = self.__url
            if debug:
                return engine_from_config(configuration=ENG_DEV_CONFIG)
            return engine_from_config(configuration=ENG_PROD_CONFIG)

    def get_session(self):
        """Returns the Session wrapped engine for this instance of EngineFactory"""
        return Session(bind=self.get_engine())


class Config:
    """
    Base configuration for the Flask Application. It includes Engine configurations for SQLAlchemy object.
    """
    # add_valid_user("USER", "PASSWORD")
    # add more valid users here
    VALID_USERS_lst = list(VALID_USERS.keys())

    # Flask
    FLASK_APP = 'wsgi.py'
    SECRET_KEY = environ.get('SECRET_KEY')
    # chrome://flags/#allow-insecure-localhost
    SSL_CONTEXT = 'adhoc'

    # Flask-Assets
    LESS_BIN = environ.get('LESS_BIN')
    ASSETS_DEBUG = environ.get('ASSETS_DEBUG')
    LESS_RUN_IN_DEBUG = environ.get('LESS_RUN_IN_DEBUG')

    # Static Assets
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    SQLALCHEMY_DATABASE_URI = EngineFactory(VALID_USERS_lst[0]).get_url()

    SQLALCHEMY_BINDS = {}
    for i in range(len(VALID_USERS_lst)):
        if "USER" in VALID_USERS_lst[i]:
            continue
        else:
            SQLALCHEMY_BINDS.update({VALID_USERS_lst[i]: EngineFactory(VALID_USERS_lst[i]).get_url()})
        pass


class ProdConfig(Config):
    """Production configuration for the Flask Application. Used to deploy the app"""

    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'hide_parameters': True,
        'pool_use_lifo': False,
        'pool_size': 20,
        'max_overflow': 0,
    }


class DevConfig(Config):
    """Development Configuration for the Flask Application. Used to test the app"""

    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
