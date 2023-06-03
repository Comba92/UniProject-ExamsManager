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


@bp.get("/<int:course>/passed")
def getStudentiPromossi(course):
  oldQuery = f"""
      SELECT * FROM Studenti s
      JOIN Compiti c USING(idStudente)
      JOIN Compiti_Validi v USING(idCompito)
      JOIN Appelli a USING(IdAppello)
      JOIN Prove p USING(idProva)
      WHERE idCorso = {course}
      GROUP BY idPercorso
      HAVING COUNT(*) >= ( SELECT DISTINCT proveDaSuperare FROM Percorsi WHERE idPercorso = p.idPercorso )
    """

  res = db.session.execute(
    db.select(Students)
      .join(Sittings)
      .join(Exams)
      .where(Sittings.passed==True)
      .group_by(Students.idStudent, Exams.idExamPath)
      .having(func.sum(Sittings.mark * (Exams.weight / 100)) >= 100)
  ).all()

  return complexQueryToList(res)