from datetime import date
from random import randint
from .models import db, Users, Students, Teachers, Courses, Subscriptions, Teaches, ExamPaths, Exams, Organizes, Reservations, Sittings

# Creazione di utenti
users = []
for i in range(1, 101):
    users.append(Users(password=f"password{i}", username=i))

# Creazione di studenti
students = []
for i in range(1, 101):
    students.append(
        Students(idStudent=i, name=f"Studente {i}", email=f"studente{i}@example.com"))

# Creazione di docenti
teachers = []
for i in range(1, 51):
    teachers.append(
        Teachers(idTeacher=i, name=f"Docente {i}", email=f"docente{i}@example.com"))

# Creazione di corsi
courses = []
for i in range(1, 21):
    courses.append(Courses(
        idCourse=i, title=f"Corso {i}", description=f"Descrizione corso {i}", academicYear=2022))

# Creazione di iscrizioni
subscriptions = []
for i in range(1, 101):
    subscriptions.append(Subscriptions(
        idStudent=i, idCourse=randint(1, 20), finalMark=randint(60, 100)))

# Creazione di insegnamenti
teaches = []
for i in range(1, 51):
    teaches.append(
        Teaches(idTeacher=i, idCourse=randint(1, 20), role="Insegnante"))

# Creazione di percorsi di esame
examPaths = []
for i in range(1, 21):
    examPaths.append(ExamPaths(idPath=i, idCourse=randint(
        1, 20), testsToPass=randint(1, 5), description=f"Percorso esame {i}"))

# Creazione di esami
exams = []
for i in range(1, 101):
    exams.append(Exams(idExam=i, idCourse=randint(1, 20), idExamPath=randint(
        1, 20), examSequenceId=i, date=date(2022, randint(1, 12), randint(1, 28))))

# Creazione di organizzazioni
organizes = []
for i in range(1, 51):
    organizes.append(Organizes(idTeacher=i, idExam=randint(1, 100)))

# Creazione di prenotazioni
reservations = []
for i in range(1, 101):
    reservations.append(Reservations(idStudent=i, idExam=randint(1, 100)))

# Creazione di sedute
sittings = []
for i in range(1, 201):
    sittings.append(Sittings(idSitting=i, idExam=randint(1, 100), idStudent=randint(
        1, 100), mark=randint(0, 100), passed=randint(0, 1), valid=randint(0, 1)))
