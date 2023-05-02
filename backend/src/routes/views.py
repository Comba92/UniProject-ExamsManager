from ..utils import *
from ..models import db
from flask import Blueprint
from sqlalchemy import text
from ..models import *

bp = Blueprint('views', __name__)

@bp.route("/")
def hello_world():
  return "<p>Hello World!</p>"


@bp.route("/prove/")
def getProve():
  res = db.session.execute(text("SELECT * FROM PROVE"))
  return resultToDict(res)


@bp.route("/utenti/")
def getUtenti():
  res = db.session.execute(text("SELECT * FROM UTENTI"))
  return resultToDict(res)


@bp.route("/testing")
def testing():
  res = db.session.execute(db.select(Utenti.username, Studenti.nome).join(Utenti).filter_by(username=88001)).all()
  for row in res:
    print(row._mapping)
  
  res = db.session.query(Utenti).all()
  for row in res:
    print(row.to_dict)

  return ''

