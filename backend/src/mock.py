from datetime import date
from random import randint
from .models import db, Users, Students, Teachers, Courses, Subscriptions, Teaches, ExamPaths, Exams, Organizes, Reservations, Sittings

def populate():
  # Creazione di utenti
  users = []
  for i in range(1, 101):
      users.append(Users(password=f"password{i}", username=i))
  db.session.add_all(users)

  # Creazione di studenti
  students = []
  for i in range(1, 51):
      students.append(
          Students(idStudent=i, name=f"Studente {i}", email=f"studente{i}@example.com"))
  db.session.add_all(students)

  # Creazione di docenti
  teachers = []
  for i in range(51, 101):
      teachers.append(
          Teachers(idTeacher=i, name=f"Docente {i}", email=f"docente{i}@example.com"))
  db.session.add_all(teachers)

  # Creazione di corsi
  courses = []
  for i in range(1, 21):
      courses.append(Courses(
          idCourse=i, title=f"Corso {i}", description=f"Descrizione corso {i}", academicYear=2022))
  db.session.add_all(courses)

  # Creazione di iscrizioni
  subscriptions = []
  for i in range(1, 101):
      subscriptions.append(Subscriptions(
          idStudent=i, idCourse=randint(1, 20), finalMark=randint(60, 100)))
  db.session.add_all(subscriptions)

  # Creazione di insegnamenti
  teaches = []
  for i in range(1, 51):
      teaches.append(
          Teaches(idTeacher=i, idCourse=randint(1, 20), role="Insegnante"))
  db.session.add_all(teaches)

  # Creazione di percorsi di esame
  examPaths = []
  for i in range(2, 21):
      examPaths.append(ExamPaths(idPath=i, idCourse=randint(
          1, 20), testsToPass=randint(1, 5), description=f"Percorso esame {i}"))
  db.session.add_all(examPaths)

  db.session.add(ExamPaths(idPath=1, idCourse=1, testsToPass=1))

  # Creazione di esami
  exams = []
  for i in range(2, 101):
      exams.append(Exams(idExam=i, idCourse=randint(1, 20), idExamPath=randint(
          1, 20), examSequenceId=i, date=date(2022, randint(1, 12), randint(1, 28)), weight=100))
  db.session.add_all(exams)
  db.session.add(Exams(idExam=1, idCourse=1, idExamPath=1, examSequenceId=1, weight=100))

  # Creazione di organizzazioni
  organizes = []
  for i in range(1, 51):
      organizes.append(Organizes(idTeacher=i, idExam=randint(1, 100)))
  db.session.add_all(organizes)

  # Creazione di prenotazioni
  reservations = []
  for i in range(1, 101):
      reservations.append(Reservations(idStudent=i, idExam=randint(1, 100)))
  db.session.add_all(reservations)

  # Creazione di sedute
  sittings = []
  for i in range(1, 201):
      sittings.append(Sittings(idSitting=i, idExam=randint(1, 100), idStudent=randint(
          1, 51), mark=randint(0, 100), passed=randint(0, 1), valid=randint(0, 1)))
  db.session.add_all(sittings)

  db.session.add(Sittings(idExam=1, idStudent=1, passed=True, valid=True, mark=70))
