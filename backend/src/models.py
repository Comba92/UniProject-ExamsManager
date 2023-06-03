from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint

db = SQLAlchemy()

class SerializableModel(db.Model):
  __abstract__ = True
  @property
  def to_dict(self):
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Users(SerializableModel):
  password = db.Column(db.String)
  username = db.Column(db.Integer, primary_key=True)

class Students(SerializableModel):
  idStudent = db.Column(db.String, db.ForeignKey(
      Users.username), primary_key=True)
  name = db.Column(db.String, nullable=False)
  email = db.Column(db.String)


class Teachers(SerializableModel):
  idTeacher = db.Column(db.String, db.ForeignKey(
      Users.username), primary_key=True)
  name = db.Column(db.String, nullable=False)
  email = db.Column(db.String)


class Courses(SerializableModel):
  idCourse = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String, nullable=False, unique=True)
  description = db.Column(db.String)
  academicYear = db.Column(db.Integer)


class Subscriptions(SerializableModel):
  idStudent = db.Column(db.Integer, db.ForeignKey(
      Students.idStudent), primary_key=True)
  idCourse = db.Column(db.Integer, db.ForeignKey(
      Courses.idCourse), primary_key=True)
  finalMark = db.Column(db.Integer)


class Teaches(SerializableModel):
  idTeacher = db.Column(db.Integer, db.ForeignKey(
      Teachers.idTeacher), primary_key=True)
  idCourse = db.Column(db.Integer, db.ForeignKey(
      Courses.idCourse), primary_key=True)
  role = db.Column(db.String)


class ExamPaths(SerializableModel):
  idPath = db.Column(db.Integer, primary_key=True)
  idCourse = db.Column(db.Integer, db.ForeignKey(
      Courses.idCourse))
  testsToPass = db.Column(db.Integer, nullable=False)
  description = db.Column(db.String)


# Appelli
class Exams(SerializableModel):
  idExam = db.Column(db.Integer, primary_key=True)
  idCourse = db.Column(db.Integer, db.ForeignKey(
    Courses.idCourse), nullable=False)
  idExamPath = db.Column(db.Integer, db.ForeignKey(ExamPaths.idPath))
  examSequenceId = db.Column(db.Integer)
  date = db.Column(db.Date)
  expiryDate = db.Column(db.Date)
  testNumber = db.Column(db.Integer)
  type = db.Column(db.String)
  description = db.Column(db.String)
  optional = db.Column(db.Boolean)
  weight = db.Column(db.Integer)


class Organizes(SerializableModel):
  idTeacher = db.Column(db.Integer, db.ForeignKey(
      Teachers.idTeacher), primary_key=True)
  idExam = db.Column(db.Integer, db.ForeignKey(
      Exams.idExam), primary_key=True)


class Reservations(SerializableModel):
  idStudent = db.Column(db.Integer, db.ForeignKey(
      Students.idStudent), primary_key=True)
  idExam = db.Column(db.Integer, db.ForeignKey(
      Exams.idExam), primary_key=True)

# Compito
class Sittings(SerializableModel):
  idSitting = db.Column(db.Integer, primary_key=True)
  idExam = db.Column(db.Integer, db.ForeignKey(
      Exams.idExam), nullable=False)
  idStudent = db.Column(db.Integer, db.ForeignKey(
      Students.idStudent), nullable=False)
  mark = db.Column(db.Integer)
  passed = db.Column(db.Boolean)
  valid = db.Column(db.Boolean)
  CheckConstraint('mark >= 0 AND mark <=100')
