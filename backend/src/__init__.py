from flask import Flask
from sqlalchemy import text

def create_app():
  app = Flask(__name__)
  app.logger.debug('Server started.')

  app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

  from .models import db
  db.init_app(app)
  app.logger.debug('Database initialized.')

  with app.app_context():
    db.drop_all()
    db.create_all()

    with app.open_resource('triggers.sql') as f:
      for trigger in f.read().decode('utf8').split('\r\n\r\n'):
        db.session.execute(text(trigger))

    with app.open_resource('queries.sql') as f:
      for query in f.read().decode('utf8').split('\r\n\r\n'):
        db.session.execute(text(query))

    db.session.commit()
    app.logger.debug('Database populated.')

  from .routes.studenti import bp as studenti
  from .routes.appelli import bp as appelli
  from .routes.corsi import bp as corsi
  from .routes.root import bp as altri

  app.register_blueprint(studenti)
  app.register_blueprint(appelli)
  app.register_blueprint(corsi)
  app.register_blueprint(altri)

  app.logger.debug('Routes built.')

  return app
