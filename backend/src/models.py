from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class SerializableModel(db.Model):
  __abstract__ = True
  @property
  def to_dict(self):
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Utenti(SerializableModel):
  username = db.Column(db.String)
  password = db.Column(db.String)
  idUtente = db.Column(db.Integer, primary_key=True)
  

class Studenti(SerializableModel):
  idStudente = db.Column(db.Integer, primary_key=True)
  idUtente = db.Column(db.Integer, db.ForeignKey(Utenti.idUtente))
  nome = db.Column(db.String, nullable=False)
  email = db.Column(db.String)


class Docenti(SerializableModel):
  idDocente = db.Column(db.Integer, primary_key=True)
  idUtente = db.Column(db.Integer, db.ForeignKey(Utenti.idUtente))
  nome = db.Column(db.String, nullable=False)
  email = db.Column(db.String)


class Corsi(SerializableModel):
  idCorso = db.Column(db.Integer, primary_key=True)
  titolo = db.Column(db.String, nullable=False)
  descrizione = db.Column(db.String)
  annoAccademico = db.Column(db.Integer)


class Iscrizione(SerializableModel):
  idStudente = db.Column(db.Integer, db.ForeignKey(
      Studenti.idStudente), primary_key=True)
  idCorso = db.Column(db.Integer, db.ForeignKey(
      Corsi.idCorso), primary_key=True)
  votoFinale = db.Column(db.Integer)


class Insegna(SerializableModel):
  idDocente = db.Column(db.Integer, db.ForeignKey(
      Docenti.idDocente), primary_key=True)
  idCorso = db.Column(db.Integer, db.ForeignKey(
      Corsi.idCorso), primary_key=True)
  ruolo = db.Column(db.String)


class Percorsi(SerializableModel):
  idPercorso = db.Column(db.Integer, primary_key=True)
  proveDaSuperare = db.Column(db.Integer, nullable=False)
  descrizione = db.Column(db.String)


class Prove(SerializableModel):
  idProva = db.Column(db.Integer, primary_key=True)
  idCorso = db.Column(db.Integer, db.ForeignKey(Corsi.idCorso), nullable=False)
  idPercorso = db.Column(db.Integer, db.ForeignKey(Percorsi.idPercorso))
  tipologia = db.Column(db.String)
  descrizione = db.Column(db.String)
  opzionale = db.Column(db.Boolean)


class Organizza(SerializableModel):
  idDocente = db.Column(db.Integer, db.ForeignKey(
      Docenti.idDocente), primary_key=True)
  idProva = db.Column(db.Integer, db.ForeignKey(
      Prove.idProva), primary_key=True)


class Appelli(SerializableModel):
  idAppello = db.Column(db.Integer, primary_key=True)
  idProva = db.Column(db.Integer, db.ForeignKey(Prove.idProva), nullable=False)
  dataEsame = db.Column(db.Date)
  dataScadenza = db.Column(db.Date)


class Compiti(SerializableModel):
  idCompito = db.Column(db.Integer, primary_key=True)
  idAppello = db.Column(db.Integer, db.ForeignKey(
      Appelli.idAppello), nullable=False)
  idStudente = db.Column(db.Integer, db.ForeignKey(
      Studenti.idStudente), nullable=False)
  voto = db.Column(db.Integer)


class CompitiValidi(SerializableModel):
  idCompito = db.Column(db.Integer, db.ForeignKey(Prove.idProva), primary_key=True)
