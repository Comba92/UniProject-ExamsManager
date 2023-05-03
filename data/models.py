"""
SQLAlchemy Data Models
These classes represent the closest abstraction to the real database,
they do not implement any kind of security (beside passwords), any control
should be made by the relative provider class before creating new instances
"""

import bcrypt
from flask_login import UserMixin
import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_sqlalchemy.session import Session
from sqlalchemy import func, text
from sqlalchemy.sql.expression import select, join, desc, or_
from sqlalchemy_utils import create_view

db = SQLAlchemy()


# Association Tables -------------------------------------------------------

# Sitting <<-- ReservedBy(Date Reserved) -->> Student (Association Table)

class SittingReservation(db.Model):
    __tablename__ = 'sitting_reservation'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"),
                        primary_key=True)
    sitting_id = db.Column(db.Integer, db.ForeignKey('sitting.id', ondelete="CASCADE"),
                           primary_key=True)
    date_reserved = db.Column(db.DateTime, index=False, nullable=False, default=datetime.datetime.utcnow())

    def __init__(self, user_id, sitting_id):
        # Check User is a student
        self.user_id = user_id
        self.sitting_id = sitting_id
        pass


# Program << -- Includes -- >> Course
class ProgramCourses(db.Model):
    __tablename__ = 'program_courses'

    program_id = db.Column(db.Integer, db.ForeignKey('program.id', ondelete="CASCADE"),
                           primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id', ondelete="CASCADE"),
                          primary_key=True)

    def __init__(self, program_id, course_id):
        # Check User is a student
        self.program_id = program_id
        self.course_id = course_id
        pass


# Course <<-- PassedBy -->> Students


# Assessment <-- AcceptedBy --> Student

class PassedCourses(db.Model):
    __tablename__ = 'passed_courses'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"),
                        primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id', ondelete="CASCADE"),
                          primary_key=True)
    date_passed = db.Column(db.DateTime, index=False, nullable=False, default=datetime.datetime.utcnow())
    final_grade = db.Column(db.Integer, nullable=False)


# Tables -------------------------------------------------------------------

class User(db.Model, UserMixin):
    """
    User Class

    It represents the users of the application. Since board members, professors and students
    have overlapping features, it is easier to differentiate their user experience by using roles.

    """

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement="auto")
    role = db.Column(db.String(128), unique=False, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String(128), nullable=False, default="Unknown")
    last_name = db.Column(db.String(128), nullable=False, default="Unknown")
    gender = db.Column(db.String, nullable=True, default="Unknown")
    birth_day = db.Column(db.DateTime, nullable=False)
    birth_city = db.Column(db.String(128), nullable=False)
    birth_province = db.Column(db.String(128), nullable=False)
    birth_country = db.Column(db.String(128), nullable=False)
    social_security_number = db.Column(db.String(128), nullable=False)
    country = db.Column(db.String(128), nullable=False)
    province = db.Column(db.String(128), nullable=False)
    city = db.Column(db.String(128), nullable=False)
    zip_code = db.Column(db.String(128), nullable=False)
    address = db.Column(db.String(128), nullable=False)
    house_number = db.Column(db.Integer, nullable=False)
    phone_number = db.Column(db.String(128), unique=True, nullable=False)
    member_since = db.Column(db.DateTime, index=False, nullable=False, default=datetime.datetime.utcnow())
    last_update = db.Column(db.DateTime, index=False, nullable=False, default=datetime.datetime.utcnow())
    last_login = db.Column(db.DateTime, index=False, nullable=False, default=datetime.datetime.utcnow())
    last_logout = db.Column(db.DateTime, index=False, nullable=True)

    # Relationships
    # User(Board) <-- Manages -->> Program
    # User(Professor) <--  Presides --> Program
    # User(Professor) <-- AssignedTo -->> Course
    # User(Student) <-- Reserves -->> Sitting
    # User(Student) <-- Accepts -->> Assessment

    pass


class Program(db.Model):
    """
    Program Class

    It represents the possible obtainable degrees in a university for each
    academic year. It has a total number of credits to obtain, in order to graduate
    and a time span. The board creates/modifies the program by including courses and
    assigning professors to them. The program can be followed by students. Students
    can follow different programs if they graduated from the previous ones.

    """

    __tablename__ = "program"

    id = db.Column(db.Integer, primary_key=True, autoincrement="auto")
    # Name of the course
    name = db.Column(db.String(256), nullable=False)
    # Credits
    credits = db.Column(db.Integer, nullable=False, default=180)
    # Academic Year of Start
    start = db.Column(db.DateTime, nullable=False)
    # Academic Year of End (After which the students are supposed to be done)
    end = db.Column(db.DateTime, nullable=False)

    # Relationships
    # Program <<-- Includes -->> Course (Association Table)
    # Program <-- FollowedBy (Graduated = False/True) -->> Student
    # Program <<-- ManagedBy --> Board (FK -> Board)
    # Program <-- PresidedBy --> Professor (FK -> Professor)

    # Constraints

    pass


class Course(db.Model):
    """
    Course Class

    It represents the course as an intermediate class to which professors are
    assigned for a certain program, during a certain academic year. The course
    is already specified with obtainable credits, whether it is divided into multiple
    modules and what semester it belongs to. Courses can have the same name if they
    have different number of modules or if they are in different academic years.

    """

    __tablename__ = "course"

    id = db.Column(db.Integer, primary_key=True, autoincrement="auto")
    # Name of the course
    name = db.Column(db.String(256), nullable=False)
    # Credits
    credits = db.Column(db.Integer, nullable=False, default=6)
    # Semester
    semester = db.Column(db.Integer, nullable=False, default=1)
    # Module
    module = db.Column(db.Integer, nullable=True, default=1)
    # Program of the course
    program = db.Column(db.Text, nullable=False, default="An Academic Course!")

    # Relationships
    # Course <<-- AssignedTo --> Professor (FK -> Professor)
    professor_fk = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"))
    # Program <<-- Includes -->> Course (Association Table)

    # Course <<-- PassedBy -->> Student (Association Table)

    # Course <-- ComposedOf -->> Exam (n>=1) (FK in Exam)

    # Constraints

    pass


class Exam(db.Model):
    """
    Exam Class

    It represents the modality of the exam(s) for a course. For the same course
    or module, a professor can create n exams which must all sum up to a total
    weight of 100. Each exam can have multiple sittings and assessments. The
    exam can have multiple parts (for multiple modules) and an order (which
    is strictly increasing from part 1 to n). Futhermore there can be a weight
    or it can be optional; in this case the weight is 1-3 additional points to
    the final grade. The professor can add a passing grade, a maximum grade (if
    the method for evaluation changes) and an expiry date after which all the exams
    which are not used for a final evaluation, become not valid and a student must
    re-sit all the exams needed for the final evaluation of the course.

    """

    __tablename__ = "exam"

    id = db.Column(db.Integer, primary_key=True, autoincrement="auto")
    # Name of the exam
    name = db.Column(db.String(128), nullable=False, default="Esame")
    # Part of the course's final evaluation (i.e. Mod.1 -> 1, ...)
    part = db.Column(db.Integer, nullable=True)
    # If it requires an order
    in_order = db.Column(db.Boolean, nullable=False, default=False)
    # Type (i.e. Oral, Project, Lab, Written ...)
    type = db.Column(db.String(128), nullable=False)
    # Weight of the exam (1-100)
    weight = db.Column(db.Integer, nullable=False, default=100)
    # If it is optional (if so the weight is 1-3)
    optional = db.Column(db.Boolean)
    # Expiry date (for exam validity)
    expiry_date = db.Column(db.DateTime, index=False, unique=False, nullable=False)

    # Relationships
    # Course <<-- Requires -->> Exam (n>=1)
    # Exam <<-- Created By --> Professor (Not needed, FK in Course)
    # Exam <-- Has -->> Sitting (FK in Sitting)

    # Constraints
    # Check that all the exams for a course sum up to 100 in percentage + 2-3 bonus points
    # If optional -> Weight is a bonus point 1-3

    pass


class Sitting(db.Model):
    """
    Sitting Class

    It represents a scheduled date for an exam, which when and where it takes place (to avoid
    reservations which collide and booking classrooms which are already full). For each sitting
    there can be a certain amount of students that can participate, and each single trial for that
    exam is then evaluate and put into Assessment by the professor. The Sitting is reserved by the
    students after the professor has published it (in the 15 days before the exam, up to 48hs before it).

    """

    __tablename__ = "sitting"

    # Basic ---------------------------------------------------------
    id = db.Column(db.Integer, primary_key=True, autoincrement="auto")
    # Building
    building = db.Column(db.String(128), nullable=False)
    # Room
    room = db.Column(db.String(128), nullable=False)
    # Start date-time
    start = db.Column(db.DateTime, nullable=False)
    # End date-time
    end = db.Column(db.DateTime, nullable=False)
    # How many students can sit it
    max_participants = db.Column(db.Integer, nullable=False, default=150)

    # Relationships
    # Sitting <-- Contains -->> Assessment
    assessments = db.relationship("Assessment", back_populates="sitting",
                                  cascade="all, delete")
    # TODO: When a

    # Sitting <<-- ReservedBy(Date Reserved) -->> Student (Association Table)

    # Exam <-- Attempted -->> Sitting (FK -> Exam)
    # Sitting <-- Contains -->> Assessment

    # Constraints
    # Start < End
    # Unique (Building, Room, Start, End)
    # Exams for 6 ECTS -> 1:30h, for 12 ECTS -> 3h

    pass


class Assessment(db.Model):
    """
    Assessment Class

    It represents the evaluation made by a professor and accepted/refused by a student.
    After the sitting is terminated, the professor can start evaluating the exams and publish
    the results. Once the results are there, the students can see their score and accept the exam.
    By default, the result is not accepted and the student must update their will to accept the result.

    """

    __tablename__ = "assessment"

    id = db.Column(db.Integer, primary_key=True, autoincrement="auto")
    grade = db.Column(db.Integer, nullable=False)
    valid = db.Column(db.Boolean, nullable=False, default=True)
    accepted = db.Column(db.Boolean, nullable=False, default=False)
    evaluation_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow())
    expiry_date_acceptance = db.Column(db.DateTime, nullable=False)

    # Relationships
    # Sitting <-- Contains -->> Assessment (FK to Assessment)
    sitting_id = db.Column(db.Integer, db.ForeignKey('sitting.id', ondelete="CASCADE"))
    sitting = db.relationship("Sitting", back_populates="assessments")

    # Assessment <-- AcceptedBy --> Student (Not worth it to put it on a different table, just use FK)
    # TODO
    # student = db.relationship("User", back_pop)

    # Constraints
    # Grade >= 18 or valid = FALSE
    # If valid = FALSE -> expiry_date_acceptance = NULL

    pass

    # TODO: Fix how we can connect the assessment to the reservation, so that we know a student was evaluated because they
    # had a reservation

# Views ------------------------------------------------------

# Professor's Views

# Student's Views
