from ..utils import *
from ..models import *
from flask import Blueprint

bp = Blueprint('views', __name__)

@bp.route("/")
def hello_world():
  return "<p>Hello World!</p>"


@bp.route("/sittings/")
def getAllSittings():
  res = db.session.query(Sittings)
  return {"query": simpleQueryToList(res)}


@bp.route("/utenti/")
def getUtenti():
  res = db.session.query(Users)
  return {"query": simpleQueryToList(res)}

