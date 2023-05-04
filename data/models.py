"""
Flask-SQLAlchemy Imperative-Mapping-Styled Database Models

These classes represent the closest abstraction to the real database,
they do not implement any kind of security, any control
should be made by the relative provider class before creating new instances.

"""

import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy_utils import create_view

db = SQLAlchemy()


# Association Tables -------------------------------------------------------

# Sitting <<-- ReservedBy(Date Reserved) -->> Student (Association Table)
class Reserves(db.Model):
    """
    Association Table for students' reservations.

    When a sitting has been published, then students can reserve a spot. Users cannot reserve
    sittings when they already have other exams at the same time, they need to delete the previous
    reservation and add a new one. Students cannot reserve the same exam for the same day twice, unless
    they delete the previous reservation.

    """

    __tablename__ = 'reserves'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"),
                        primary_key=True)
    sitting_id = db.Column(db.Integer, db.ForeignKey('sitting.id', ondelete="CASCADE"),
                           primary_key=True)
    date_reserved = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow())
    pass


# Program <<-- Includes -->> Course
class Includes(db.Model):
    """
    Association Table for the courses belonging to a program. A course might be included in multiple programs, and
    programs have many courses.

    """

    __tablename__ = 'includes'

    program_id = db.Column(db.Integer, db.ForeignKey('program.id', ondelete="CASCADE"),
                           primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id', ondelete="CASCADE"),
                          primary_key=True)
    pass


# Student <<-- Follows -->> Course
class Follows(db.Model):
    """
    Association Table for the courses followed by the students. The student may follow different course (even courses
    that are not strictly related to the programs they follow) and if they pass the course, their final grade is
    memorized when the conditions for final evaluation are met (valid, not expired...).


    """

    __tablename__ = 'follows'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"),
                        primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id', ondelete="CASCADE"),
                          primary_key=True)
    final_grade = db.Column(db.Integer, nullable=False)
    registry_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow())
    pass


# Student <-- Subscribes --> Program
class Subscribes(db.Model):
    """
    Association Table for the students' programs. A student may be subscribed to multiple programs as long as
    only one program has no final grade and no registry date. When a student graduates, the final grade is registered.

    """

    __tablename__ = 'subscribes'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"),
                        primary_key=True)
    program_id = db.Column(db.Integer, db.ForeignKey('program.id', ondelete="CASCADE"),
                           primary_key=True)
    final_grade = db.Column(db.Integer, nullable=True)
    registry_date = db.Column(db.DateTime, nullable=True)
    pass


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
    password_hash = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String(128), nullable=False, default="Unknown")
    last_name = db.Column(db.String(128), nullable=False, default="Unknown")
    birth_day = db.Column(db.DateTime, nullable=False)
    birth_address = db.Column(db.String, nullable=False)
    social_security_number = db.Column(db.String(128), nullable=False)
    address = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String(128), unique=True, nullable=False)
    member_since = db.Column(db.DateTime, index=False, nullable=False, default=datetime.datetime.utcnow())
    last_update = db.Column(db.DateTime, index=False, nullable=False, default=datetime.datetime.utcnow())
    last_login = db.Column(db.DateTime, index=False, nullable=False, default=datetime.datetime.utcnow())
    last_logout = db.Column(db.DateTime, index=False, nullable=True)

    # Relationships
    # User(Board) <-- Manages -->> Program
    programs_created = db.relationship("Programs", back_populates="board")
    # Student <<-- Subscribes -->> Program (More if they have graduated)
    programs = db.relationship('Subscribes', foreign_keys=[Subscribes.program_id],
                               back_populates="students",
                               lazy='dynamic',
                               cascade='all, delete')
    # User(Board) <-- Creates -->> Courses
    courses_created = db.relationship("Course", back_populates="board")
    # User(Professor) <--  Presides --> Program
    # User(Professor) <-- AssignedTo -->> Course
    courses = db.relationship("Course", back_populates="professor")
    # User(Student) <<-- Follows -->> Courses
    followed = db.relationship('Follows', foreign_keys=[Follows.course_id],
                               back_populates="students",
                               lazy='dynamic',
                               cascade='all, delete')
    # User(Student) <<-- Reserves -->> Sitting
    reservations = db.relationship('Reserves', foreign_keys=[Reserves.sitting_id],
                                   back_populates="bookers",
                                   lazy='dynamic',
                                   cascade='all, delete')
    # User(Student) <-- Accepts -->> Assessment
    assessments = db.relationship("Assessment", back_populates="student")
    
    def __init__(self, data):
        role = data.get('role')
        email = data.get('email')
        password_hash = data.get('password_hash')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        birth_day = data.get('birth_day')
        birth_address = data.get('birth_address')
        social_security_number = data.get('ssn')
        address = data.get('address')
        phone_number = data.get('phone_number')
        member_since = db.Column(db.DateTime, index=False, nullable=False, default=datetime.datetime.utcnow())
        last_update = db.Column(db.DateTime, index=False, nullable=False, default=datetime.datetime.utcnow())
        last_login = db.Column(db.DateTime, index=False, nullable=False, default=datetime.datetime.utcnow())
        pass
    
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
    # Program <<-- CreatedBy --> Board
    board_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    board = db.relationship("User", back_populates="programs_created")
    # Program <<-- Includes -->> Course (Association Table)
    courses = db.relationship('Includes', foreign_keys=[Includes.course_id],
                              back_populates="programs",
                              lazy='dynamic',
                              cascade='all, delete')
    # Student <<-- Subscribes -->> Program (More if they have graduated)
    students = db.relationship('Subscribes', foreign_keys=[Subscribes.user_id],
                               back_populates="programs",
                               lazy='dynamic',
                               cascade='all, delete')
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
    # Course <<-- CreatedBy --> Board
    board_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    board = db.relationship("User", back_populates="courses_created")
    # Course <<-- AssignedTo --> Professor (FK -> Professor)
    professor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    professor = db.relationship("User", back_populates="courses")
    # Program <<-- Includes -->> Course (Association Table)
    programs = db.relationship('Includes', foreign_keys=[Includes.program_id],
                               back_populates="courses",
                               lazy='dynamic',
                               cascade='all, delete')
    # Course <<-- PassedBy -->> Student (Association Table)
    students = db.relationship('Follows', foreign_keys=[Follows.user_id],
                               back_populates="followed",
                               lazy='dynamic',
                               cascade='all, delete')
    # Course <-- ComposedOf -->> Exam (n>=1) (FK in Exam)
    exams = db.relationship("Exam", back_populates="course", cascade="all, delete")
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
    # Exam <<-- Created By --> Professor (Not needed, FK in Course)
    # Course <-- Requires -->> Exam (n>=1)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id', ondelete="CASCADE"))
    course = db.relationship("Course", back_populates="exams")
    # Exam <-- Has -->> Sitting (FK in Sitting)
    sittings = db.relationship("Sitting", back_populates="exam", cascade="all, delete")

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
    # How many students can sit it (for a trigger before insert)
    max_participants = db.Column(db.Integer, nullable=False, default=150)

    # Relationships
    # Exam <-- Attempted -->> Sitting (FK -> Exam)
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.id', ondelete="CASCADE"))
    exam = db.relationship("Exam", back_populates="sittings")
    # Student <<-- Reserves -->> Sitting (Association Table)
    bookers = db.relationship('Reserves', foreign_keys=[Reserves.user_id],
                              back_populates="reservations",
                              lazy='dynamic',
                              cascade='all, delete')
    # Sitting <-- Contains -->> Assessment
    assessments = db.relationship("Assessment", back_populates="sitting", cascade="all, delete")

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
    the results (insert). Once the results are there, the students can see their score and accept the exam (update).
    By default, the result is not accepted and the student must update their will to accept the result.

    """

    __tablename__ = "assessment"

    id = db.Column(db.Integer, primary_key=True, autoincrement="auto")
    grade = db.Column(db.Integer, nullable=False)
    # True if grade >= passing grade
    valid = db.Column(db.Boolean, nullable=False, default=True)
    evaluation_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow())
    # Default 10 days from evaluation date, after which the exam expires
    expiry_acceptance_date = db.Column(db.DateTime, nullable=False)
    # Modified by student when they accept it
    # NULL -> failed, True -> accepted, False -> rejected/expired
    accepted = db.Column(db.Boolean, nullable=True)
    acceptance_date = db.Column(db.DateTime, nullable=True)

    # Relationships
    # Assessment <<-- RefersTo --> Sitting (FK to Assessment)
    sitting_id = db.Column(db.Integer, db.ForeignKey('sitting.id', ondelete="CASCADE"))
    sitting = db.relationship("Sitting", back_populates="assessments")
    # Assessment <<-- AcceptedBy --> Student (If the reservation was made)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"))
    student = db.relationship("User", back_populates="assessments")

    def __init__(self, grade: int, valid: bool, ):
        pass

    pass

# Views ------------------------------------------------------

# Professor's Views
#
# 1) - View for professor's courses
# prof_id, email, course_id, course_name, academic_year,
#
# 2) - View for exams to evaluate
#
# 3) - View for exams evaluated
#
# 4) - Stats for exams

# Student's Views
# 0) - View for student's study plan
# student_id, email, program_id, program_name, course_id, course_name,
# 1) - View for student's exam reservations
# student_id, email, course_id, course_name, module, part, starting_date, end_date, building, room
# 2) - View for exams to be accepted
#
# 3) - View for registered exams
# student_id, email, course_id, course_name, final_grade, date_registered
# 4) - View for all exams done
# student_id, email, course_id, course_name, module, part, grade, valid, accepted
# 5) - View stats for career
