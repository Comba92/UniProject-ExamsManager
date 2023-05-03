from ..utils import *
from ..models import *
from flask import Blueprint, request

bp = Blueprint('exams', __name__, url_prefix='/exams')

@bp.get("/")
def getExams():
  res = db.session.query(Exams)
  return {"query": simpleQueryToList(res)}


@bp.post("/<int:exam>/reserve")
def reserveExam(exam):
  req = request.get_json()
  newSubscription = Reservations(
      idStudent=req['idStudent'],
      idCourse=exam
  )
  res = db.session.add(newSubscription)

  db.session.commit()
  return {"stats": "success"}


@bp.get("/<int:appello>/accepted")
def getPassedStudents(exam):
  res = db.session.execute(
    db.select(Students)
      .join(Sittings)
      .join(Exams)
      .where(Exams.idExam==exam, Sittings.accepted)
  ).all()

  return {"query": complexQueryToList(res)}
