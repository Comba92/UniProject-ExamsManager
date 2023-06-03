INSERT INTO Users (username)
VALUES ('88001'), ('88002'), ('88003'), ('99001');

INSERT INTO Students (name, idStudent)
VALUES ('marco', '88001'), ('giulio', '88002'), ('andrea', '88003');

INSERT INTO Teachers (name, idTeacher)
VALUES ('prof', '99001');

INSERT INTO TEACHES (idTeacher, idCourse)
VALUES ('99001', 1), ('99001', 2), ('99001', 3)

INSERT INTO Courses (title)
VALUES ('informatica'), ('matematica'), ('statistica');

INSERT INTO Subscriptions (idCourse, idStudent)
VALUES (1, '88001'), (1, '88002'), (2, '88002'), (2, '88003'), (3, '88001')

INSERT INTO Exam_Paths (testsToPass)
VALUES (3), (2), (1), (2), (1);

INSERT INTO Exams (idCourse, idExamPath)
VALUES (1, 1), (1, 1), (1, 1), (1, 2), (1, 2), (1, 3), (2, 4), (2, 5);

INSERT INTO Sittings (idExam, idStudent, passed)
VALUES (1, '88001', true), (1, '88002', false), (3, '88001', true), (8, '88001', false), (2, '88002', false), (2, '88003', true), (4,'88002', true), (1, '88003', true), (4, '88003', true), (5, '88003', true);