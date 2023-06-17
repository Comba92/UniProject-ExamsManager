from ..utils import *
from ..models import *
from flask import Blueprint, request
from sqlalchemy import func
from .courses import getCourses

bp = Blueprint('students', __name__, url_prefix='/students')

@bp.get("/")
def getStudents():
  res = db.session.query(Students)
  return simpleQueryToList(res)


@bp.get("/<int:student>/")
def getStudentData(student):
  res = db.session.query(Students).filter_by(idStudent=student).one()
  return res.to_dict


@bp.get("/<int:student>/subscribed/")
def getSubscribedCourses(student):
  res = db.session.execute(
    db.select(Courses)
    .join(Subscriptions)
    .where(Subscriptions.idStudent == student)
  ).all()

  return complexQueryToList(res)


@bp.get("/<int:student>/courses/")
def getNotSubscribedCourses(student):
  courses = getCourses()
  subscribed = getSubscribedCourses(student)
  return [item for item in courses if item not in subscribed]


@bp.post("/<int:student>/subscribe")
def subscribeFromCourse(student):
  req = request.get_json()

  subscription = Subscriptions(idStudent=student, idCourse=req['idCourse'])

  db.session.add(subscription)
  db.session.commit()
  return {"status": "success"}


@bp.post("/<int:student>/unsubscribe")
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


@bp.get("/<int:student>/exams/")
def getSubscribedExams(student):
  res = db.session.execute(
      db.select(Exams, Courses)
      .join(Courses)
      .join(Subscriptions)
      .join(Students)
      .where(Students.idStudent == student)
      .where(Exams.idExam.not_in(
        db.select(Reservations.idExam)
        .where(Reservations.idStudent == student)
      ))
  ).all()

  return complexQueryToList(res)


@bp.get("/<int:student>/reserved/")
def reservedExams(student):
  res = db.session.execute(
      db.select(Reservations, Exams, Courses)
      .select_from(Reservations)
      .join(Exams)
      .join(Courses)
      .where(Reservations.idStudent == student)
  ).all()

  return complexQueryToList(res)

@bp.post("/<int:student>/reserve")
def reserveExam(student):
  req = request.get_json()

  reservation = Reservations(idStudent=student, idExam=req['idExam'])

  db.session.add(reservation)
  db.session.commit()
  return {"status": "success"}


@bp.post("/<int:student>/unreserve")
def unreserverExam(student):
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

  return complexQueryToList(res)


@bp.get("/<int:student>/history/")
def getExamsHistory(student):
  res = db.session.execute(
      db.select(Sittings)
      .join(Students)
      .where(Sittings.idStudent == student)
  ).all()
  
  return complexQueryToList(res)


@bp.get("/<int:student>/marks/")
def getStudentMarks(student):
  res = db.session.execute(
    db.select(Subscriptions, Courses)
      .join(Students)
      .join(Courses)
      .where(Students.idStudent==student)
  ).all()

  return complexQueryToList(res)


# The hard one
@bp.get("/<int:student>/toValidate/")
def getStudentMarksToAccept(student):
  res = db.session.execute(
    db.select(Courses, func.sum(Sittings.mark * Exams.weight / 100).label("markToValidate"))
      .select_from(Sittings)
      .join(Exams)
      .join(ExamPaths)
      .join(Courses)
      .where(Sittings.valid==True, Exams.optional==False, Sittings.idStudent==student)
      .group_by(ExamPaths.idPath)
      .having(func.count()==ExamPaths.testsToPass)
  )
  # returns a list of all courses where all my markes are valid and the count is equal to the exam paths testsToPass

  return complexQueryToList(res)


@bp.post("/<int:student>/validate/")
def validateMark(student):
  req = request.get_json()

  course = db.select(Subscriptions).filter_by(idStudent=student)
  course.finalMark = req['finalMark']
  db.session.commit()

  return {'status': 'success'}
