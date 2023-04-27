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
  return resultToDict(res)


@app.get("/studenti/<studente>/esiti/")
def getProveValideStudente(studente):
  res = db.session.execute(text(
    f"""
      SELECT * FROM Compiti_Validi
      JOIN Compiti USING(idCompito)
      WHERE idStudente = {studente}
    """
  ))
  return resultToDict(res)


@app.get("/studenti/<studente>/storico/")
def getStoricoStudente(studente):
  res = db.session.execute(text(
    f"""
      SELECT * FROM Compiti
      WHERE idStudente = {studente}
    """
  ))
  return resultToDict(res)


@app.get("/corsi/")
def getCorsi():
  res = db.session.execute(text("SELECT * FROM Corsi"))
  return resultToDict(res)


@app.get("/corsi/<corso>/prove")
def getProveCorso(corso):
  res = db.session.execute(text(
    f"""
      SELECT Prove.* FROM Prove
      JOIN Corsi USING(idCorso)
      WHERE idCorso = {corso}
    """
  ))
  return resultToDict(res)


@app.get("/corsi/<corso>/promossi")
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


@app.get("/docenti/")
def getDocenti():
  res = db.session.execute(text("SELECT * FROM Docenti"))
  return resultToDict(res)


@app.get("/appelli/")
def getAppelli():
  res = db.session.execute(text("SELECT * FROM Appelli"))
  return resultToDict(res)


@app.get("/appelli/<appello>/positivi")
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


@app.get("/prove/")
def getProve():
  res = db.session.execute(text("SELECT * FROM PROVE"))
  return resultToDict(res)

def resultToDict(queryResult):
  return {"results": [dict(row._mapping) for row in queryResult]}

def filterBy(queryResult, column, value):
  d = resultToDict(queryResult)
  f = list(filter(lambda tupla: tupla[column] == int(value), d["results"]))
  return { "results": f }