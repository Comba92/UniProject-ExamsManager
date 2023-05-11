# UniExamHandler Project

## Requirements

| _Requirements_                       | **Mandatory** | Done | Tested |
|--------------------------------------|---------------|------|--------|
| Logic Schema                         |       Y       |      |        |
| Relational Schema                    |       Y       |      |        |
| Relational Database                  |       Y       |      |        |
| Front End (HTML, CSS)                |       Y       |      |        |
| Front End (Js)                       |               |      |        |
| Back End `Flask`                     |       Y       |      |        |
| Back End `SQLAlchemy`                |       Y       |      |        |
| Back End `Flask-SQLAlchemy`          |       Y       |      |        |
| Constraints                          |       Y       |      |        |
| Triggers                             |       Y       |      |        |
| Transactions                         |               |      |        |
| Roles                                |       Y       |      |        |
| Authorization Policies               |               |      |        |
| Authentication Policy                |               |      |        |
| Security XSS, SQL Injection, CRSF... |               |      |        |
| Indices                              |               |      |        |
| Materialized Views                   |               |      |        |
| ORM                                  |       Y       |      |        |

Implementation:
* Schema
  * Logic, Relational
* Database
  * Supabase PostgreSQL
* Front End
  * HTML, CSS, Javascript
* Back End
  * Flask, Flask-SQLAlchemy, SQLALchemy
* Data Integrity
  * Constraints
  * Triggers
  * Transactions
* Security
  * Roles
  * Authorization Policies
  * Authentication Policy
  * Defense against XSS, SQL Injection, CRSF, ...
* Optimization
  * Indices
  * Materialized Views
* Abstraction
  * ORM
  
---

## Set Up

### Environment - Python
Tested with Python 3.9, SQLAlchemy 2.0, Flask 3.0

### Requirements - Pip

```shell
pip install -r requirements.txt
```

### .env
Create a file `.env` in the root directory as follows

```text
# SUPABASE

DRIVER = "postgresql"
DIALECT = "postgres"
USER = "postgres"
PASSWORD =  "UniExamHandler"
HOST = "db.anepkhaszxisnudysyzw.supabase.co"
PORT_DIRECT = "5432"
DATABASE = "postgres"

# Roles and Connections
BOARD = "board"
BOARD_PSW = "wq223ttgrdas"

PROF = "professor"
PROF_PSW = "wqer325yhlk"

STUD = "student"
STUD_PSW = "tr34q56F43"

ADMIN = "admin"
ADMIN_PSW = "dsf210tlkl"
``` 

---

## Schema 

### Logic Schema

![]()

### Relational Schema

![]()

---

## Supabase - Relational Database (PostgreSQL)

If supabase fails to connect 

https://github.com/supabase/supabase/issues/7938

---

## Front End

### Implementation
* Blueprints

### Routes`UniExamHandler.com/`

#### All

| Login **Not** Required        | **Login Required**                            |
|-------------------------------|-----------------------------------------------|
| `/welcome`, Landing page      | `/dashboard` (changes for each one of  them)  |
| `/about`, About the project   | `/profile`, Check/Update/Remove personal data |
| `/credits`, About the authors | `/statistics` (changes for each one of them)  |
| `/register`, Register form    |                                               |
| `/login`, Login form          |                                               |
|                               |                                               |

#### Board - Login Required

| **Board Role Required**                     | _Description_                                                                                     |
|---------------------------------------------|---------------------------------------------------------------------------------------------------|
| `/<board>/programs`                         | All the programs, the count of students who follow it, the academic year, the credits...          |
| `/<board>/programs/add`                     | Add new program (then add course)                                                                 |
| `/<board>/<program>/students`               | All the students, the final score if they graduated,...                                           |
| `/<board>/<program>/professors`             | All the professors and the courses                                                                |
| `/<board>/<program>/delete`                 | Remove program (then go back to programs)                                                         |
| `/<board>/<program>/courses`                | All the courses, the professors, the count of students who follow it, the credits, the modules... |
| `/<board>/<program>/courses/add-course`     | Add course to program (and professor)                                                             |
| `/<board>/<program>/courses/create-course`  | Creates and adds new course to program (and professor)                                            |
| `/<board>/<program>/<course>/remove-course` | Remove course from program                                                                        |
| `/<board>/<program>/<course>/results`       | All the final scores for each student                                                             |
| `/<board>/professors`                       | All the professors                                                                                |
| `/<board>/professors/add`                   | Add new professor                                                                                 |
| `/<board>/professors/remove`                | Remove professor                                                                                  |
| `/<board>/<professor>/courses`              | All the courses for a professor                                                                   |
| `/<board>/students`                         | All the students                                                                                  |

#### Professor - Login Required

| **Professor Role Required**                              | _Description_                                                                |
|----------------------------------------------------------|------------------------------------------------------------------------------|
| `/<professor>/courses`                                   | All the courses the professor is assigned to                                 |
| `/<professor>/<course>/evaluations`                      | The final scores of the students and their evaluation dates, accepted or not |
|                                                          | (If there are two modules, both professors can see this)                     |
| `/<professor>/<course>/exams`                            | All the exams created for a course                                           |
| `/<professor>/<course>/exams/add`                        | Where we can add exams for a course                                          |
| `/<professor>/<course>/exams/delete`                     | Where we can remove exams for a course                                       |
| `/<professor>/<course>/<exam>/evaluations`               | The exam scores of the students and their evaluation dates, accepted or not  |
| `/<professor>/<course>/<exam>/sittings`                  | All the sittings created for an exam                                         |
| `/<professor>/<course>/<exam>/sittings/add`              | Where we can add sittings                                                    |
| `/<professor>/<course>/<exam>/sittings/delete`           | Where we can remove sittings                                                 |
| `/<professor>/<course>/<exam>/<sitting>/bookings`        | All the bookings                                                             |
| `/<professor>/<course>/<exam>/<sitting>/assessments`     | All the assessments to evaluate (only a view)                                |
| `/<professor>/<course>/<exam>/<sitting>/assessments/add` | Where we can update the assessments (creation of assessment)                 |

#### Student - Login Required

| **Student Role Required**                 | _Description_                                                                                                   |
|-------------------------------------------|-----------------------------------------------------------------------------------------------------------------|
| `/<student>/career`                       | Summary of the program's information, final graduation score (if present), academic year..                      |
| `/<student>/career/add-program`           | Subscribe to a program (when new or graduated)                                                                  |
| `/<student>/career/remove-program`        | Unsubscribe to a program                                                                                        |
| `/<student>/studyplan`                    | All the courses from the programs (extra too), and their final score (from where we can accept the final score) |
| `/<student>/studyplan/add-course`         | Add extra course                                                                                                |
| `/<student>/studyplan/remove-course`      | Remove extra course (cannot remove mandatory courses)                                                           |
| `/<student>/booking`                      | All the possible exams dates to book, from where we can book them                                               |
| `/<student>/booking/add-reservation`      | Add reservation                                                                                                 |
| `/<student>/booking/reservations`         | All the reservations made, and if they were canceled                                                            |
| `/<student>/booking/<reservation>/remove` | Remove reservation                                                                                              |
| `/<student>/assessments`                  | All the recent results (before the exam is accepted), from where we can accept the exam                         |
| `/<student>/<assessment>/accept`          | Accept assessment                                                                                               |
| `/<student>/<assessment>/refuse`          | Refuse assessment                                                                                               |
| `/<student>/results`                      | All the past results (course, exam, ..., result, valid, ...)                                                    |

---

## Backend


---

## TODO


1. Controller per certe query (studentExists, etc...)
2. Trigger per controllo una sola prova valida per appello
3. Trigger eliminazione prova valida dopo scadenza

4. Rifare schemi, la tabella NonValidi e' inutile e non e' necessaria

---

## Tests

Test 1:
1. Launch app
2. Welcome
3. Register -> Profile
4. Profile

---

## Weak points
* Security - Login
* SQL Injection, CRSF
* Timezone absent in dates
* Server-Side Roles
  * https://tableplus.com/blog/2018/04/postgresql-how-to-grant-access-to-users.html
  * https://www.postgresql.org/docs/current/ddl-priv.html#:~:text=PostgreSQL%20grants%20privileges%20on%20some,%2C%20tablespaces%2C%20or%20configuration%20parameters.
  * https://stackoverflow.com/questions/22288581/managing-user-privileges-in-sqlalchemy