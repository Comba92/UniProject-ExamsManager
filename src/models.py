from init import db

class Studenti(db.Model):
  idStudente = db.Column(db.Integer, primary_key=True)
  nome = db.Column(db.String, nullable=False)


class Docenti(db.Model):
  idDocente = db.Column(db.Integer, primary_key=True)
  nome = db.Column(db.String, nullable=False)


class Corsi(db.Model):
  idCorso = db.Column(db.Integer, primary_key=True)
  titolo = db.Column(db.String, nullable=False)
  proveDaSuperare = db.Column(
      db.Integer, db.CheckConstraint("proveDaSuperare >= 1"), nullable=False
  )


class Insegna(db.Model):
  idDocente = db.Column(db.Integer, db.ForeignKey(
      Docenti.idDocente), primary_key=True)
  idCorso = db.Column(db.Integer, db.ForeignKey(
      Corsi.idCorso), primary_key=True)


class Appelli(db.Model):
  idAppello = db.Column(db.Integer, primary_key=True)
  dataEsame = db.Column(db.Date, nullable=False)
  idCorso = db.Column(db.Integer, db.ForeignKey(Corsi.idCorso), nullable=False)


class Prove(db.Model):
  idProva = db.Column(db.Integer, primary_key=True)
  voto = db.Column(db.Integer, nullable=False)
  idAppello = db.Column(db.Integer, db.ForeignKey(
      Appelli.idAppello), nullable=False)
  idStudente = db.Column(db.Integer, db.ForeignKey(
      Studenti.idStudente), nullable=False)
  superata = db.Column(db.Boolean, nullable=False)


class ProveValide(db.Model):
  dataScadenza = db.Column(db.Date, nullable=False)
  idProva = db.Column(db.Integer, db.ForeignKey(
      Prove.idProva), nullable=False,  primary_key=True)
