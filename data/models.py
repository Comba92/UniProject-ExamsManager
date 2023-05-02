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


# Association Tables

# Course << -- TaughtBy -- >> Professor

#

# Tables


class User(db.Model, UserMixin):
    """User Class"""

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement="auto")
    email = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    first_name = db.Column(db.String(128), unique=False, nullable=True, default="Unknown")
    last_name = db.Column(db.String(128), unique=False, nullable=True, default="Unknown")

    gender = db.Column(db.String(128), unique=False, nullable=True, default="Unknown")
    birth_day = db.Column(db.DateTime, unique=False, nullable=False)
    birth_city = db.Column(db.String(128), unique=False, nullable=False)
    birth_province = db.Column(db.String(128), unique=False, nullable=False)
    birth_country = db.Column(db.String(128), unique=False, nullable=False)
    social_security_number = db.Column(db.String(128), unique=False, nullable=False)

    country = db.Column(db.String(128), unique=False, nullable=False)
    province = db.Column(db.String(128), unique=False, nullable=False)
    city = db.Column(db.String(128), unique=False, nullable=False)
    zip_code = db.Column(db.Integer)
    address = db.Column(db.String(128), unique=False, nullable=False)
    house_number = db.Column(db.Integer)
    house_phone_number = db.Column(db.String(128), unique=False, nullable=False)
    personal_phone_number = db.Column(db.String(128), unique=False, nullable=False)

    member_since = db.Column(db.DateTime, index=False, unique=False, nullable=True,
                             default=datetime.datetime.utcnow())
    last_update = db.Column(db.DateTime, index=False, unique=False, nullable=False,
                            default=datetime.datetime.utcnow())
    last_login = db.Column(db.DateTime, index=False, unique=False, nullable=False,
                           default=datetime.datetime.utcnow())
    last_logout = db.Column(db.DateTime, index=False, unique=False, nullable=True)

    # Relationships ---------------------------------------------------------

    def __init__(self, data=None):
        """
        Initialize User from dictionary. Assumes all parameters are coherent with the database constraints.
        :param data: dictionary with keys "role", "username", "email", "password", "first_name", "last_name",
        "gender", "region", "bio", "group"
        """
        if data is None:
            data = {}
        if len(data) == 0:
            raise RuntimeError("Cannot initialize User with empty data field")

        self.__set_role(data['role'])

        if 'group' in list(data.keys()):
            self.__set_group(data['group'])
        else:
            # Listener or Premium
            self.group_id = None

        self.name = data['username']
        self.email = data['email']
        self.password_hash = data['password']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.gender = data['gender']
        self.region = data['region']
        self.bio = data['bio']
        self.member_since = datetime.datetime.utcnow()
        self.last_update = datetime.datetime.utcnow()
        self.last_login = datetime.datetime.utcnow()
        self.last_logout = None
        pass

    def to_dict(self):
        """
        Returns self as a dictionary
        :return: dictionary with keys 'id', 'name','role_id','email','password_hash','group_id', 'member_since',
        'last_update','last_login', 'last_logout'
        """
        return {
            'id': self.id,
            'name': self.name,
            'role_id': self.role_id,
            'email': self.email,
            'password_hash': self.password_hash,
            'group_id': self.group_id,
            'member_since': self.member_since,
            'last_update': self.last_update,
            'last_login': self.last_login,
            'last_logout': self.last_logout,
        }


#
# class Program(db.Model):
#     pass


class Course(db.Model):
    """
    Course Class

    It represents the course for an academic year in terms of
    assignments/exams needed to pass the course. The professor(s) who
    are assigned to a course are responsible for its modalities and can
    create exams/assignments or other evaluations. There is at least one exam
    and one professor per course.
    """

    __tablename__ = "course"

    id = db.Column(db.Integer, primary_key=True, autoincrement="auto")
    # Name of the course
    name = db.Column(db.String(256), nullable=False)
    # Academic Year
    year = db.Column(db.Integer, nullable=False)
    # Exams needed to pass
    exams = db.Column(db.Integer, nullable=False)

    # Relationships
    # Degree <<-- Include -->> Course (sum up to 180 ects or 120 ...)
    # Course <<-- ComposedOf -->> Exam (n>=1)
    # Course <<-- FollowedBy -->> Student, it includes the final mark when the student has accepted the final mark
    # Student that has accepted a final mark cannot follow again the course.

    # Constraints
    # Unique tuple (name, year)

    pass


class Exam(db.Model):
    """
    Exam Class

    It represents a kind of assignment/exam needed for a course's final
    evaluation. It can have multiple sittings and can be re-sit, but all
    the exams need to be valid and not expired for the final evaluation to
    be created (so that the student can accept the final mark).

    """

    __tablename__ = "exam"

    id = db.Column(db.Integer, primary_key=True, autoincrement="auto")
    # Name of the exam
    name = db.Column(db.String(128), nullable=False)
    # Part of the course's final evaluation (i.e. Mod.1 -> 1, ...)
    part = db.Column(db.Integer)
    # Type (i.e. Oral, Project, Lab, Written ...)
    type = db.Column(db.String(128), nullable=False)
    # Weight of the exam (1-100)
    weight = db.Column(db.Integer)
    # If it is optional
    optional = db.Column(db.Boolean)
    # Date for the sittings
    sitting_date = db.Column(db.DateTime, index=False, unique=False, nullable=False,
                             default=datetime.datetime.utcnow())
    # Expiry date (for exam validity)
    expiry_date = db.Column(db.DateTime, index=False, unique=False, nullable=False)
    # Last date to accept the exam's result
    acceptance_date = db.Column(db.DateTime, index=False, unique=False, nullable=False)
    # Passing grade
    passing = db.Column(db.Integer, nullable=False, default=18)

    # Relationships
    # Course <<-- ComposedOf -->> Exam (n>=1)
    # Exam <<-- PlannedBy -->> Professor (n>=1)
    # Exam <-- Has -->> Sitting

    # Constraints
    # Check that all the exams for a course sum up to 100 in percentage + 2-3 bonus points
    # If optional -> Weight is a bonus point 1-3

    pass


class Sitting(db.Model):
    """
    Sitting Class

    It represents a sitting for an exam (since exams can have multiple
    dates).

    """

    __tablename__ = "sitting"

    # Basic ---------------------------------------------------------
    id = db.Column(db.Integer, primary_key=True, autoincrement="auto")
    # Class

    # Start date-time

    # End date-time

    # Final grade
    grade = db.Column(db.Integer)
    # Accepted
    accepted = db.Column(db.Boolean)
    # Valid
    valid = db.Column(db.Boolean)

    # Relationships
    # Sitting <<-- References --> Exam
    # Sitting <<-- Evaluates --> Student

    pass


# Views ------------------------------------------------------
