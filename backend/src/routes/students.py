from ..utils import *
from ..models import *
from flask import Blueprint, request

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

@bp.post("/<int:student>/unsubscribe")
def unsubscribeFromCourse(student):
  req = request.get_json()

  isSubscribedTo = (
    db.select(Subscriptions.idCourse)
      .where(Subscriptions.idStudent == student, Subscriptions.idCourse == req['idCourse'])
  )

  db.first_or_404(isSubscribedTo)

  db.session.execute(
    db.delete(Subscriptions)
      .where(Subscriptions.idCourse.in_(isSubscribedTo))
  )

  try:
    db.session.commit()
    return {"status": "success"}
  except:
    return {"status": "error"}


@bp.get("/<int:student>/results/")
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
