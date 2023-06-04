from ..utils import *
from ..models import *
from flask import Blueprint, request
from .students import getStudentData
from .teachers import getTeacherData

bp = Blueprint('login', __name__)


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

