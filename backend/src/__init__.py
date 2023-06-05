from flask import Flask
from sqlalchemy import text
from flask_cors import CORS

from .mock import populate

def create_app():
  app = Flask(__name__)
  CORS(app)
  app.logger.debug('Server started.')

  app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
  app.config["SECRET_KEY"] = "bdd2023"

  from .models import db
  db.init_app(app)
  app.logger.debug('Database initialized.')

  with app.app_context():
    db.drop_all()
    db.create_all()

    """ with app.open_resource('queries.sql') as f:
      for query in f.read().decode('utf8').split('\r\n\r\n'):
        db.session.execute(text(query)) """
    
    populate()

    db.session.commit()
    app.logger.debug('Database populated.')

  from .routes.students import bp as students
  from .routes.teachers import bp as teachers
  from .routes.exams import bp as exams
  from .routes.courses import bp as courses
  from .routes.views import bp as views
  from .routes.login import bp as login

  app.register_blueprint(students)
  app.register_blueprint(teachers)
  app.register_blueprint(exams)
  app.register_blueprint(courses)
  app.register_blueprint(views)
  app.register_blueprint(login)

  app.logger.debug('Routes built.')

  return app
