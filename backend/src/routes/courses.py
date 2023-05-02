from ..utils import *
from ..models import *
from flask import Blueprint
from sqlalchemy import func

bp = Blueprint('courses', __name__, url_prefix='/courses')

@bp.get("/")
def getCourses():
  res = db.session.query(Courses)
  return {"query": simpleQueryToList(res)}


@bp.get("/<int:course>/tests")
def getCourseTests(course):
  res = db.session.execute(
    db.select(Tests)
      .join(Courses)
      .where(Courses.idCourse==course)
  )
  return {"query": complexQueryToList(res)}


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
      .join(Tests)
      .where(Sittings.accepted==True)
      .group_by(Students.idStudent, Tests.idExamPath)
      .having(func.sum(Sittings.mark * (Tests.weight / 100)) >= 100)
  ).all()

  return {"query": complexQueryToList(res)}
