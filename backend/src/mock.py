from datetime import date
from random import randint
from .models import db, Users, Students, Teachers, Courses, Subscriptions, Teaches, ExamPaths, Exams, Organizes, Reservations, Sittings

# Creazione di utenti
user1 = Users(password="password1", username=1)
user2 = Users(password="password2", username=2)
user3 = Users(password="password3", username=3)

# Creazione di studenti
student1 = Students(idStudent=1, name="Studente 1",
                    email="studente1@example.com")
student2 = Students(idStudent=2, name="Studente 2",
                    email="studente2@example.com")

# Creazione di docenti
teacher1 = Teachers(idTeacher=1, name="Docente 1",
                    email="docente1@example.com")
teacher2 = Teachers(idTeacher=2, name="Docente 2",
                    email="docente2@example.com")

# Creazione di corsi
course1 = Courses(idCourse=1, title="Corso 1",
                  description="Descrizione corso 1", academicYear=2022)
course2 = Courses(idCourse=2, title="Corso 2",
                  description="Descrizione corso 2", academicYear=2022)

# Creazione di iscrizioni
subscription1 = Subscriptions(idStudent=1, idCourse=1, finalMark=90)
subscription2 = Subscriptions(idStudent=2, idCourse=2, finalMark=85)

# Creazione di insegnamenti
teaches1 = Teaches(idTeacher=1, idCourse=1, role="Insegnante")
teaches2 = Teaches(idTeacher=2, idCourse=2, role="Insegnante")

# Creazione di percorsi di esame
examPath1 = ExamPaths(idPath=1, idCourse=1, testsToPass=2,
                      description="Percorso esame 1")
examPath2 = ExamPaths(idPath=2, idCourse=2, testsToPass=3,
                      description="Percorso esame 2")

# Creazione di esami
exam1 = Exams(idExam=1, idCourse=1, idExamPath=1, examSequenceId=1, date=date(2022, 6, 1), expiryDate=date(
    2022, 6, 15), testNumber=2, type="Scritto", description="Esame 1", optional=False, weight=50)
exam2 = Exams(idExam=2, idCourse=2, idExamPath=2, examSequenceId=1, date=date(2022, 6, 1), expiryDate=date(
    2022, 6, 15), testNumber=3, type="Orale", description="Esame 2", optional=True, weight=30)

# Creazione di organizzazioni
organizes1 = Organizes(idTeacher=1, idExam=1)
organizes2 = Organizes(idTeacher=2, idExam=2)

# Creazione di prenotazioni
reservation1 = Reservations(idStudent=1, idExam=1)
reservation2 = Reservations(idStudent=2, idExam=2)

# Creazione di sedute
sitting1 = Sittings(idSitting=1, idExam=1, idStudent=1,
                    mark=randint(60, 100), passed=True, valid=True)
sitting2 = Sittings(idSitting=2, idExam=2, idStudent=2,
                    mark=randint(60, 100), passed=False, valid=True)

# Aggiunta dei record al database
db.session.add_all([user1, user2, user3, student1, student2, teacher1, teacher2, course1, course2, subscription1, subscription2,
                   teaches1, teaches2, examPath1, examPath2, exam1, exam2, organizes1, organizes2, reservation1, reservation2, sitting1, sitting2])
db.session.commit()
