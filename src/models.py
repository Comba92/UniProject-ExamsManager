from init import db


class Studenti(db.Model):
  idStudente = db.Column(db.Integer, primary_key=True)
  nome = db.Column(db.String, nullable=False)
  email = db.Column(db.String)


class Docenti(db.Model):
  idDocente = db.Column(db.Integer, primary_key=True)
  nome = db.Column(db.String, nullable=False)
  email = db.Column(db.String)


class Corsi(db.Model):
  idCorso = db.Column(db.Integer, primary_key=True)
  titolo = db.Column(db.String, nullable=False)
  annoAccademico = db.Column(db.Integer)


class Iscrizione(db.Model):
  idStudente = db.Column(db.Integer, db.ForeignKey(
      Studenti.idStudente), primary_key=True)
  idCorso = db.Column(db.Integer, db.ForeignKey(
      Corsi.idCorso), primary_key=True)


class Insegna(db.Model):
  idDocente = db.Column(db.Integer, db.ForeignKey(
      Docenti.idDocente), primary_key=True)
  idCorso = db.Column(db.Integer, db.ForeignKey(
      Corsi.idCorso), primary_key=True)


class Percorsi(db.Model):
  idPercorso = db.Column(db.Integer, primary_key=True)
  proveDaSuperare = db.Column(db.Integer, nullable=False)
  descrizione = db.Column(db.String)


class Prove(db.Model):
  idProva = db.Column(db.Integer, primary_key=True)
  idCorso = db.Column(db.Integer, db.ForeignKey(Corsi.idCorso), nullable=False)
  idPercorso = db.Column(db.Integer, db.ForeignKey(Percorsi.idPercorso))
  tipologia = db.Column(db.String)
  opzionale = db.Column(db.Boolean)


class Organizza(db.Model):
  idDocente = db.Column(db.Integer, db.ForeignKey(
      Docenti.idDocente), primary_key=True)
  idProva = db.Column(db.Integer, db.ForeignKey(
      Prove.idProva), primary_key=True)


class Appelli(db.Model):
  idAppello = db.Column(db.Integer, primary_key=True)
  idProva = db.Column(db.Integer, db.ForeignKey(Prove.idProva), nullable=False)
  dataEsame = db.Column(db.Date)
  dataScadenza = db.Column(db.Date)


class Compiti(db.Model):
  idCompito = db.Column(db.Integer, primary_key=True)
  idAppello = db.Column(db.Integer, db.ForeignKey(
      Appelli.idAppello), nullable=False)
  idStudente = db.Column(db.Integer, db.ForeignKey(
      Studenti.idStudente), nullable=False)
  voto = db.Column(db.Integer)


class CompitiValidi(db.Model):
  idCompito = db.Column(db.Integer, db.ForeignKey(Prove.idProva), primary_key=True)
