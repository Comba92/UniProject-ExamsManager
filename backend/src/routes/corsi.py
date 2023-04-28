from ..utils import *
from ..models import db
from flask import Blueprint
from sqlalchemy import text

bp = Blueprint('corsi', __name__, url_prefix='/corsi')

@bp.get("/")
def getCorsi():
  res = db.session.execute(text("SELECT * FROM Corsi"))
  return resultToDict(res)


@bp.get("/<int:corso>/prove")
def getProveCorso(corso):
  res = db.session.execute(text(
      f"""
      SELECT Prove.* FROM Prove
      JOIN Corsi USING(idCorso)
      WHERE idCorso = {corso}
    """
  ))
  return resultToDict(res)


@bp.get("/<corso>/promossi")
def getStudentiPromossi(corso):
  res = db.session.execute(text(
      f"""
      SELECT * FROM Studenti s
      JOIN Compiti c USING(idStudente)
      JOIN Compiti_Validi v USING(idCompito)
      JOIN Appelli a USING(IdAppello)
      JOIN Prove p USING(idProva)
      WHERE idCorso = {corso}
      GROUP BY idPercorso
      HAVING COUNT(*) >= ( SELECT DISTINCT proveDaSuperare FROM Percorsi WHERE idPercorso = p.idPercorso )
    """
  ))

  return resultToDict(res)
