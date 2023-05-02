from ..utils import *
from ..models import *
from flask import Blueprint

bp = Blueprint('teachers', __name__, url_prefix='/teachers')

@bp.get("/")
def getTeachers():
  res = db.session.query(Teachers)
  return {"query": simpleQueryToList(res)}


@bp.get("/<int:teacher>/")
def getTeacherData(teacher):
  res = db.session.query(Teachers).filter_by(idTeacher=teacher).one()
  return {"query": res.to_dict}
