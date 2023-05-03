INSERT INTO Users (username)
VALUES ('88001'), ('88002'), ('88003'), ('99001');

INSERT INTO Students (name, idStudent)
VALUES ('marco', 1), ('giulio', 2), ('andrea', 3);

INSERT INTO Teachers (name, idTeacher)
VALUES ('prof', 4);

INSERT INTO Courses (title)
VALUES ('informatica'), ('matematica'), ('statistica');

INSERT INTO Subscriptions (idCourse, idStudent)
VALUES (1, 1), (1, 2), (2, 2), (2, 3), (3, 1)

INSERT INTO Exam_Paths (testsToPass)
VALUES (3), (2), (1), (2), (1);

INSERT INTO Tests (idCourse, idExamPath)
VALUES (1, 1), (1, 1), (1, 1), (1, 2), (1, 2), (1, 3), (2, 4), (2, 5);

INSERT INTO Exams (idTest)
VALUES (1), (2), (3), (4), (5), (6), (7), (8);

INSERT INTO Sittings (idExam, idStudent)
VALUES (1, 1), (1, 2), (3, 1), (8, 1), (2, 2), (2, 3), (4, 2), (1, 3), (4, 3), (5, 3);