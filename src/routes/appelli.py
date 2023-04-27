from ..utils import *
from ..models import db
from flask import Blueprint
from sqlalchemy import text

bp = Blueprint('appelli', __name__, url_prefix='/appelli')

@bp.get("/")
def getAppelli():
  res = db.session.execute(text("SELECT * FROM Appelli"))
  return resultToDict(res)


@bp.get("/<int:appello>/positivi")
def getStudentiPositiviAppello(appello):
  res = db.session.execute(text(
      f"""
      SELECT Studenti.* FROM Studenti
      JOIN Compiti USING(idStudente)
      JOIN Compiti_Validi USING(idCompito)
      JOIN Appelli USING(idAppello)
      WHERE idAppello = {appello}
    """
  ))
  return resultToDict(res)
