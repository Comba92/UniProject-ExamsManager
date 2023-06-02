from ..utils import *
from ..models import *
from flask import Blueprint, request
from .students import getStudentData
from .teachers import getTeacherData

bp = Blueprint('login', __name__)

@bp.post('/old_login')
def old_login():
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


@bp.post('/login')
def login():
  req = request.get_json()
  print(req)

  if req['type'] == 'STUDENT':
    userToLogin = db.one_or_404(
        db.select(Users)
          .join(Students)
          .where(Users.username==req['username'])
    )
    return getStudentData(userToLogin.username)
  
  elif req['type'] == 'TEACHER':
    userToLogin = db.one_or_404(
        db.select(Users)
          .join(Teachers)
          .where(Users.username==req['username'])
    )
    return getTeacherData(userToLogin.username)

