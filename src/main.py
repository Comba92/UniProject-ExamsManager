from init import app, db
from models import *
from datetime import date
from sqlalchemy import text, DDL

with app.app_context():
  db.create_all()

@app.route("/")
def hello_world():
  return "<p>Hello World!</p>"


@app.get("/prove")
def getProve():
  res = db.session.execute(text(
    """
      SELECT * FROM Prove
      LEFT JOIN Prove_Valide USING(idProva)
    """
  ))
  return resultToJson(res)

@app.get("/studenti")
def getStudenti():
  res = db.session.execute(text("SELECT * FROM Studenti"))
  return resultToJson(res)

@app.get("/studenti/<studente>/prove")
def getProveValideStudente(studente):
  res = db.session.execute(text(
    f"""
      SELECT * FROM Prove_Valide v
      JOIN Prove p USING(idProva)
      WHERE p.idStudente = {studente}
    """
  ))
  return resultToJson(res)

@app.get("/studenti/<studente>/storico")
def getStoricoStudente(studente):
  res = db.session.execute(text(
    f"""
      SELECT p.* FROM Prove p
      WHERE p.idStudente = {studente}
    """
  ))
  return resultToJson(res)

@app.get("/corsi")
def getCorsi():
  res = db.session.execute(text("SELECT * FROM Corsi"))
  return resultToJson(res)

@app.get("/corsi/<esame>/voti")
def getVotiNonConfermatiEsame(esame):
  res = db.session.execute(text(
    f"""
      SELECT * FROM Studenti s
      JOIN Prove p USING(idStudente)
      WHERE p.idProva IN (SELECT idProva FROM Prove_Valide)
      GROUP BY s.idStudente
      HAVING COUNT(*) = (
        SELECT DISTINCT proveDaSuperare FROM Corsi
        JOIN Appelli Using(idCorso)
        WHERE idAppello = p.idAppello AND idCorso = {esame}
      )
    """
  ))
  return resultToJson(res)


@app.get("/docenti")
def getDocenti():
  res = db.session.execute(text("SELECT * FROM Docenti"))
  return resultToJson(res)

@app.get("/appelli")
def getAppelli():
  res = db.session.execute(text("SELECT * FROM Appelli"))
  return resultToJson(res)


@app.get("/appelli/passati")
def getStatoAppelli():
  res = db.session.execute(text(
    """
      SELECT a.*, s.* FROM Appelli a
      JOIN Prove p USING(idAppello)
      JOIN Prove_Valide USING(idProva)
      JOIN Studenti s USING(idStudente)
      GROUP BY a.idAppello
    """
  ))
  return resultToJson(res)


@app.get("/dummy")
def randomData():
  stuff = []
  stuff.append(Studenti(nome='giulio', idStudente=234))
  stuff.append(Studenti(nome='andrea', idStudente=123))
  stuff.append(Studenti(nome='marco', idStudente=345))
  stuff.append(Corsi(titolo="Informatica", proveDaSuperare=2))
  stuff.append(Appelli(idCorso=1, dataEsame=date.today()))
  stuff.append(Prove(voto=1, idStudente=345, idAppello=1, superata=True))
  stuff.append(Prove(voto=2, idStudente=345, idAppello=1, superata=True))
  stuff.append(Prove(voto=3, idStudente=345, idAppello=1, superata=False))
  stuff.append(Prove(voto=4, idStudente=123, idAppello=1, superata=True))
  stuff.append(Prove(voto=5, idStudente=234, idAppello=1, superata=True))
  stuff.append(Prove(voto=6, idStudente=234, idAppello=1, superata=False))
  stuff.append(ProveValide(idProva=1, dataScadenza=date.today()))
  stuff.append(ProveValide(idProva=2, dataScadenza=date.today()))
  stuff.append(ProveValide(idProva=5, dataScadenza=date.today()))
  for s in stuff:
    db.session.add(s)
  db.session.commit()

  return '', 200

def resultToJson(res):
  return {"results": [dict(row._mapping) for row in res]}