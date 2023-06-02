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
  return simpleQueryToList(res)


@bp.route("/users/")
def getUtenti():
  res = db.session.query(Users)
  return simpleQueryToList(res)

