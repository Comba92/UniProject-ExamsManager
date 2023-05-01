from ..utils import *
from ..models import db
from flask import Blueprint
from sqlalchemy import text

bp = Blueprint('studenti', __name__, url_prefix='/studenti')

@bp.get("/")
def getStudenti():
  res = db.session.execute(text("SELECT * FROM Studenti"))
  return resultToDict(res)


@bp.get("/<int:studente>/esiti/")
def getProveValideStudente(studente):
  res = db.session.execute(text(
      f"""
        SELECT * FROM Compiti_Validi
        JOIN Compiti USING(idCompito)
        WHERE idStudente = {studente}
      """
  ))
  return resultToDict(res)


@bp.get("/<int:studente>/storico/")
def getStoricoStudente(studente):
  res = db.session.execute(text(
    f"""
      SELECT * FROM Compiti
      WHERE idStudente = {studente}
    """
  ))
  return resultToDict(res)
