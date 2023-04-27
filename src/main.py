from init import app, db
from models import *
import queries
from datetime import date
from sqlalchemy import text, DDL

with app.app_context():
  db.drop_all()
  db.create_all()
  for query in queries.populate:
    db.session.execute(text(query))
  db.session.commit()

@app.route("/")
def hello_world():
  return "<p>Hello World!</p>"


@app.get("/studenti/")
def getStudenti():
  res = db.session.execute(text("SELECT * FROM Studenti"))
  return resultToJson(res)


@app.get("/studenti/<studente>/compiti/")
def getProveValideStudente(studente):
  res = db.session.execute(text(
    f"""
      SELECT * FROM Compiti_Validi
      JOIN Compiti USING(idCompito)
      WHERE idCompito = {studente}
    """
  ))
  return resultToJson(res)


@app.get("/studenti/<studente>/storico/")
def getStoricoStudente(studente):
  res = db.session.execute(text(
    f"""
      SELECT * FROM Compiti
      WHERE idStudente = {studente}
    """
  ))
  return resultToJson(res)


@app.get("/corsi/")
def getCorsi():
  res = db.session.execute(text("SELECT * FROM Corsi"))
  return resultToJson(res)


@app.get("/prove/")
def getProve():
  res = db.session.execute(text("SELECT * FROM PROVE"))
  return resultToJson(res)


@app.get("/corsi/<corso>/prove")
def getProveCorso(corso):
  res = db.session.execute(text(
    f"""
      SELECT * FROM Prove
      JOIN Corsi USING(idCorso)
      WHERE idCorso = {corso}
    """
  ))
  return resultToJson(res)


@app.get("/docenti/")
def getDocenti():
  res = db.session.execute(text("SELECT * FROM Docenti"))
  return resultToJson(res)


@app.get("/appelli/")
def getAppelli():
  res = db.session.execute(text("SELECT * FROM Appelli"))
  return resultToJson(res)


def resultToJson(res):
  return {"results": [dict(row._mapping) for row in res]}