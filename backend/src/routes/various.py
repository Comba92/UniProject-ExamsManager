from ..utils import *
from ..models import db
from flask import Blueprint
from sqlalchemy import text

bp = Blueprint('various', __name__)

@bp.route("/")
def hello_world():
  return "<p>Hello World!</p>"


@bp.get("/docenti/")
def getDocenti():
  res = db.session.execute(text("SELECT * FROM Docenti"))
  return resultToDict(res)


@bp.get("/prove/")
def getProve():
  res = db.session.execute(text("SELECT * FROM PROVE"))
  return resultToDict(res)
