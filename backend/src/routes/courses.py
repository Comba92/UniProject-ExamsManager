from ..utils import *
from ..models import *
from flask import Blueprint, request
from sqlalchemy import func

bp = Blueprint('courses', __name__, url_prefix='/courses')

@bp.get("/")
def getCourses():
  res = db.session.query(Courses)
  return simpleQueryToList(res)


@bp.get("/<int:course>/exams")
def getCourseTests(course):
  res = db.session.execute(
    db.select(Exams)
      .join(Courses)
      .where(Courses.idCourse==course)
  )
  return complexQueryToList(res)


@bp.get("/<int:course>/paths")
def getCoursePaths(course):
  res = db.session.execute(
      db.select(ExamPaths)
      .join(Courses)
      .where(Courses.idCourse == course)
  )
  return complexQueryToList(res)


@bp.post("/<int:course>/subscribe")
def subscribeToCourse(course):
  req = request.get_json()
  newSubscription = Subscriptions(
    idStudent = req['idStudent'],
    idCourse = course
  )
  res = db.session.add(newSubscription)

  db.session.commit()
  return {"stats": "success"}
