from ..utils import *
from ..models import *
from flask import Blueprint, request
from sqlalchemy import func

bp = Blueprint('students', __name__, url_prefix='/students')

@bp.get("/")
def getStudents():
  res = db.session.query(Students)
  return {"query": simpleQueryToList(res)}

@bp.get("/<int:student>/")
def getStudentData(student):
  res = db.session.query(Students).filter_by(idStudent=student).one()
  return {"query": res.to_dict}


@bp.get("/<int:student>/courses/")
def getSubscribedCourses(student):
  res = db.session.execute(
    db.select(Courses)
      .join(Subscriptions)
      .join(Students)
      .where(Students.idStudent == student)
  ).all()

  return {"query": complexQueryToList(res)}


@bp.delete("/<int:student>/unsubscribe")
def unsubscribeFromCourse(student):
  req = request.get_json()

  isSubscribedTo = (
    db.select(Subscriptions.idCourse)
      .where(Subscriptions.idStudent == student, Subscriptions.idCourse == req['idCourse'])
  )

  db.first_or_404(isSubscribedTo)

  res = db.session.execute(
    db.delete(Subscriptions)
      .where(Subscriptions.idCourse.in_(isSubscribedTo))
  )

  db.session.commit()
  return {"status": "success"}


@bp.delete("/<int:student>/unreserve")
def unsubscribeFromCourse(student):
  req = request.get_json()

  isReservedTo = (
      db.select(Reservations.idExam)
      .where(Subscriptions.idStudent == student, Reservations.idExam == req['idExam'])
  )

  db.first_or_404(isReservedTo)

  res = db.session.execute(
      db.delete(Reservations)
      .where(Reservations.idExam.in_(isReservedTo))
  )

  db.session.commit()
  return {"status": "success"}


@bp.get("/<int:student>/valids/")
def getExamsResults(student):
  res = db.session.execute(
    db.select(Sittings)
      .join(Students)
      .where(Sittings.idStudent==student, Sittings.valid==True)
  ).all()

  return {"query": complexQueryToList(res)}


@bp.get("/<int:student>/history/")
def getExamsHistory(student):
  res = db.session.execute(
      db.select(Sittings)
      .join(Students)
      .where(Sittings.idStudent == student)
  ).all()
  
  return {"query": complexQueryToList(res)}


@bp.get("/<int:student>/marks/")
def getStudentMarks(student):
  res = db.session.execute(
    db.select(Subscriptions)
      .join(Students)
      .where(Students.idStudent==student)
  ).all()

  return {"query": complexQueryToList(res)}


# The hard one
@bp.get("/<int:student>/results/")
def getStudentMarksToAccept(student):
  res = db.session.execute(
    db.select(Sittings)
      .join(Students)
      .join(Exams)
      .join(Tests)
      .where(Students.idStudent==student, Sittings.valid==True)
      .group_by(Students.idStudent, Tests.idExamPath)
      .having(func.sum(Sittings.mark * (Tests.weight/100)) >= 100)
  ).all()

  return {"query": complexQueryToList(res)}
