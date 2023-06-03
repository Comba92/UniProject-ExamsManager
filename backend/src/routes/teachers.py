from ..utils import *
from ..models import *
from flask import Blueprint, request

bp = Blueprint('teachers', __name__, url_prefix='/teachers')

@bp.get("/")
def getTeachers():
  res = db.session.query(Teachers)
  return simpleQueryToList(res)


@bp.get("/<int:teacher>/")
def getTeacherData(teacher):
  res = db.session.query(Teachers).filter_by(idTeacher=teacher).one()
  return res.to_dict


@bp.get("/<int:teacher>/courses")
def getTeachedCourses(teacher):
  res = db.session.execute(
      db.select(Courses)
      .join(Teaches)
      .where(Teaches.idTeacher == teacher)
  ).all()

  return complexQueryToList(res)


@bp.get("/<int:teacher>/exams")
def getCoursesExams(teacher):
  res = db.session.execute(
      db.select(Exams)
      .join(Courses)
      .join(Teaches)
      .where(Teaches.idTeacher == teacher)
  ).all()

  return complexQueryToList(res)


@bp.get("/<int:teacher>/sittings")
def getSittings(teacher):
  res = db.session.execute(
      db.select(Sittings)
      .join(Exams)
      .join(Courses)
      .join(Teaches)
      .where(Teaches.idTeacher == teacher)
  ).all()

  return complexQueryToList(res)

@bp.get("/<int:teacher>/exams/<int:exam>/students")
def getCoursesExamStudents(teacher, exam):
  res = db.session.execute(
    db.select(Students)
      .join(Sittings)
      .join(Exams)
      .join(Courses)
      .join(Teaches)
      .where(Teaches.idTeacher == teacher, Exams.idExam == exam)
  ).all()

  return complexQueryToList(res)


@bp.post("/<int:teacher>/createCourse/")
def createCourse(teacher):
  req = request.get_json()
  newCourse = Courses(
      title=req['title']
  )
  db.session.add(newCourse)
  db.session.commit()

  relation = Teaches(
    idCourse=newCourse.idCourse,
    idTeacher=teacher
  )

  db.session.add(relation)
  db.session.commit()

  return {"status": "success"}

@bp.post("/<int:teacher>/createExam/")
def createExam(teacher):
  req = request.get_json()
  newExam = Exams(
      idCourse=req['idCourse'],
  )
  db.session.add(newExam)
  db.session.commit()

  relation = Organizes(
      idExam=newExam.idExam,
      idTeacher=teacher
  )
  db.session.add(relation)
  db.session.commit()

  return {"status": "success"}


@bp.post("/<int:teacher>/assignMark")
def assignMark(teacher):
  req = request.get_json()
  sitting = (
    Sittings.query
      .join(Exams)
      .join(Courses)
      .join(Teaches)
      .where(Teaches.idTeacher == teacher, Sittings.idSitting==req['idSitting'])
  ).one()

  sitting.mark = req['mark']
  db.session.commit()

  return {"status": "success"}