from ..utils import *
from ..models import *
from flask import Blueprint

bp = Blueprint('exams', __name__, url_prefix='/exams')

@bp.get("/")
def getExams():
  res = db.session.query(Exams)
  return {"query": simpleQueryToList(res)}


@bp.get("/<int:appello>/accepted")
def getPassedStudents(exam):
  res = db.session.execute(
    db.select(Students)
      .join(Sittings)
      .join(Exams)
      .where(Exams.idExam==exam, Sittings.accepted)
  ).all()

  return {"query": complexQueryToList(res)}
