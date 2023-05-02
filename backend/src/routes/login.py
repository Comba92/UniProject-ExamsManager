from ..utils import *
from ..models import db
import functools
from flask import Blueprint, request
from sqlalchemy import text


bp = Blueprint('login', __name__)

@bp.post('/login')
def login():
  req = request.get_json()
  user = db.session.execute(text(
    f"""
      SELECT * FROM Utenti
      WHERE username = {req['username']}
    """ 
  ))

  userInDB = resultToDict(user)['results']
  if len(userInDB) == 0:
    return {'error': 'user not found'}, 401

  userInDB = userInDB[0]
  if req['type'] == 'STUDENT':
    studente = db.session.execute(text(
      f"""
        SELECT * FROM Studenti
        WHERE idUtente = {userInDB['idUtente']}
      """
    ))  
    return resultToDict(studente)
  
  elif req['type'] == 'TEACHER':
    docente = db.session.execute(text(
      f"""
        SELECT * FROM Docenti
        WHERE idUtente = {userInDB['idUtente']}
      """
    ))
    return resultToDict(docente)
