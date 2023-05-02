from ..utils import *
from ..models import db
from flask import Blueprint
from sqlalchemy import text

bp = Blueprint('docenti', __name__, url_prefix='/docenti')

@bp.get("/")
def getDocenti():
  res = db.session.execute(text("SELECT * FROM Docenti"))
  return resultToDict(res)
