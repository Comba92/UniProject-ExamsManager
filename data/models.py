"""
Flask-SQLAlchemy Imperative-Mapping-Styled Database Models

These classes represent the closest abstraction to the real database,
they do not implement any kind of security, any control
should be made by the relative provider class before creating new instances.

"""

import datetime
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

# Association Tables -------------------------------------------------------

# Student <<-- Reserves -->> Sitting
reserves = db.Table(
    'reserves', db.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('sitting_id', db.Integer, db.ForeignKey('sitting.id', ondelete='CASCADE'), primary_key=True),
    db.Column('date_reserved', db.DateTime, nullable=False, default=datetime.datetime.utcnow()),
    comment='Association Table for students\' reservations. When a sitting has been published, '
            'then students can reserve a spot. Users cannot reserve sittings when they already '
            'have other exams at the same time, they need to delete the previous reservation '
            'and add a new one. Students cannot reserve the same exam for the same day twice, '
            'unless they delete the previous reservation.')

# Program <<-- Includes -->> Course
includes = db.Table(
    'includes', db.metadata,
    db.Column('program_id', db.Integer, db.ForeignKey('program.id', ondelete='CASCADE'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id', ondelete='CASCADE'), primary_key=True),
    comment='Association Table for the courses belonging to a program. '
            'A course might be included in multiple board, and board have many courses.')

# Student <<-- Follows -->> Course
follows = db.Table(
    'follows', db.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id', ondelete='CASCADE'), primary_key=True),
    db.Column('final_grade', db.Integer, nullable=True),
    db.Column('registry_date', db.DateTime, nullable=True),
    comment='Association Table for the courses followed by the students. '
            'The student may follow different course (even courses '
            'that are not strictly related to the board they follow) '
            'and if they pass the course, their final grade is memorized '
            'when the conditions for final evaluation are met (valid, not expired...)')

# Student <<-- Subscribes -->> Program
subscribes = db.Table(
    'subscribes', db.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('program_id', db.Integer, db.ForeignKey('program.id', ondelete='CASCADE'), primary_key=True),
    db.Column('final_grade', db.Integer, nullable=True),
    db.Column('registry_date', db.DateTime, nullable=True),
    comment='Association Table for the students\' board. '
            'A student may be subscribed to multiple board as long as'
            'only one program has no final grade and no registry date. '
            'When a student graduates, the final grade is registered.')

user_roles = db.Table(
    'user_roles', db.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id', ondelete='CASCADE'), primary_key=True),
    comment='Association Table for user\'s roles')


# Tables -------------------------------------------------------------------


class Role(db.Model):
    """
    Role Class

    Defines possible user actions based on the role
    """

    __tablename__ = "role"

    id = db.Column(db.Integer, primary_key=True, autoincrement="auto")
    name = db.Column(db.String, unique=True, nullable=False)

    # Relationships
    # User <<-- Has -->> Role
    users = db.relationship('User',
                            secondary=user_roles,
                            back_populates='roles')

    def __init__(self, data):
        # TODO: define the permissions for later usage on routes @roles_required
        # https://flask-user.readthedocs.io/en/latest/authorization.html
        self.name = data.get('name')
        pass

    def __repr__(self):
        return f'<Role: {self.name}>'
    #
    # def to_dict(self) -> dict:
    #     data = {
    #         'id': self.id,
    #         'name': self.name
    #     }
    #     return data

    pass


class User(db.Model, UserMixin):
    """
    User Class

    It represents the users of the application. Since board members, professors and students
    have overlapping features, it is easier to differentiate their user experience by using roles.

    """

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement="auto")
    email = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String(128), nullable=False, default="Unknown")
    last_name = db.Column(db.String(128), nullable=False, default="Unknown")
    # birth_day = db.Column(db.DateTime, nullable=False)
    # birth_address = db.Column(db.String, nullable=False)
    # social_security_number = db.Column(db.String(128), nullable=False)
    # address = db.Column(db.String, nullable=False)
    member_since = db.Column(db.DateTime, index=False, nullable=False, default=datetime.datetime.utcnow())
    last_update = db.Column(db.DateTime, index=False, nullable=False, default=datetime.datetime.utcnow())
    last_login = db.Column(db.DateTime, index=False, nullable=False, default=datetime.datetime.utcnow())
    last_logout = db.Column(db.DateTime, index=False, nullable=True)

    # Relationships

    # User(Professor) <-- AssignedTo -->> Course
    assigned_to = db.relationship(argument='Course',
                                  back_populates='professor')
    # User(Student) <-- Accepts -->> Assessment
    evaluations = db.relationship(argument='Assessment',
                                  back_populates='student')
    # User(Student) <<-- Subscribes -->> Program (More if they have graduated)
    programs = db.relationship(argument='Program',
                               secondary=subscribes,
                               back_populates='students')
    # User(Student) <<-- Follows -->> Courses
    courses = db.relationship(argument='Course',
                              secondary=follows,
                              back_populates='students')
    # User(Student) <<-- Reserves -->> Sitting
    reservations = db.relationship(argument='Sitting',
                                   secondary=reserves,
                                   back_populates='bookers')
    # User <<-- Has -->> Roles
    roles = db.relationship(argument='Role',
                            secondary=user_roles,
                            back_populates='users')

    def __init__(self, data):
        # self.role = data.get('role')
        self.email = data.get('email')
        self.password_hash = data.get('password_hash')
        self.first_name = data.get('first_name')
        self.last_name = data.get('last_name')
        # self.birth_day = data.get('birth_day')
        # self.birth_address = data.get('birth_address')
        # self.social_security_number = data.get('ssn')
        # self.address = data.get('address')
        # self.phone_number = data.get('phone_number')
        self.member_since = datetime.datetime.utcnow()
        self.last_update = datetime.datetime.utcnow()
        self.last_login = datetime.datetime.utcnow()
        self.last_logout = None
        pass

    def __repr__(self):
        return f'<User: {self.email}>'

    # @staticmethod
    # def load(user_id):
    #     return None

    # def to_dict(self) -> dict:
    #     """
    #     Returns dictionary with user's information
    #
    #     :return: dictionary
    #     """
    #     data = {
    #         'email': self.email,
    #         'password_hash': self.password_hash,
    #         'first_name': self.first_name,
    #         'last_name': self.last_name,
    #         'birth_day': self.birth_day,
    #         'birth_address': self.birth_address,
    #         'address': self.address,
    #         'ssn': self.social_security_number,
    #         'phone_number': self.phone_number,
    #         'member_since': self.member_since,
    #         'last_update': self.last_update,
    #         'last_login': self.last_login,
    #         'last_logout': self.last_logout,
    #     }
    #     return data

    def get_id(self) -> int:
        return self.id

    pass


class Program(db.Model):
    """
    Program Class

    It represents the possible obtainable degrees in a university for each
    academic year. It has a total number of credits to obtain, in order to graduate
    and a time span. The board creates/modifies the program by including courses and
    assigning professors to them. The program can be followed by students. Students
    can follow different board if they graduated from the previous ones.

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
    courses = db.relationship(argument='Course',
                              secondary=includes,
                              back_populates='programs')
    # Student <<-- Subscribes -->> Program (More if they have graduated)
    students = db.relationship(argument='User',
                               secondary=subscribes,
                               back_populates='programs')

    def __init__(self, data):
        self.name = data.get('name')
        self.credits = data.get('credits')
        self.start = data.get('start')
        self.end = data.get('end')
        pass

    def __repr__(self):
        return f'<Program: {self.name}>'

    def to_dict(self) -> dict:
        data = {'id': self.id,
                'name': self.name,
                'credits': self.credits,
                'start': self.start,
                'end': self.end}
        return data

    # @staticmethod
    # def load(program_id):
    #     return db.select(Program).filter_by(id=program_id)

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

    # Relationships
    # Course <<-- AssignedTo --> Professor (FK -> Professor)
    professor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    professor = db.relationship(argument='User',
                                back_populates="assigned_to")
    # Program <<-- Includes -->> Course (Association Table)
    programs = db.relationship(argument='Program',
                               secondary=includes,
                               back_populates='courses')
    # Course <<-- PassedBy -->> Student (Association Table)
    students = db.relationship(argument='User',
                               secondary=follows,
                               back_populates='courses')
    # Course <-- ComposedOf -->> Exam (n>=1) (FK in Exam)
    exams = db.relationship(argument='Exam',
                            back_populates='course',
                            cascade='all, delete')

    # Constraints

    def __init__(self, data):
        self.name = data.get('name')
        self.credits = int(data.get('credits'))
        self.semester = int(data.get('semester'))
        self.module = int(data.get('module'))
        pass

    # def __repr__(self):
    #     return f'<Course: {self.name}>'
    #
    # def to_dict(self) -> dict:
    #     data = {'id': self.id,
    #             'name': self.name,
    #             'credits': self.credits,
    #             'semester': self.semester,
    #             'module': self.module}
    #     return data
    #
    # @staticmethod
    # def load(self):
    #     pass

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
    optional = db.Column(db.Boolean, default=False)
    # Expiry date (for exam validity)
    expiry_date = db.Column(db.DateTime, index=False, unique=False, nullable=False,
                            default=(datetime.datetime.utcnow() + datetime.timedelta(days=100)))

    # Relationships
    # Course <-- Requires -->> Exam (n>=1)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id', ondelete="CASCADE"))
    course = db.relationship(argument='Course',
                             back_populates="exams")
    # Exam <-- Has -->> Sitting (FK in Sitting)
    sittings = db.relationship(argument='Sitting',
                               back_populates="exam",
                               cascade="all, delete")

    # Constraints
    # Check that all the exams for a course sum up to 100 in percentage + 2-3 bonus points
    # If optional -> Weight is a bonus point 1-3

    def __repr__(self):
        return f'<Exam: {self.name}>'

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
    end = db.Column(db.DateTime, nullable=False, default=(start + datetime.timedelta(hours=2)))
    # How many students can sit it (for a trigger before insert)
    max_participants = db.Column(db.Integer, nullable=False, default=150)

    # Relationships
    # Exam <-- Attempted -->> Sitting (FK -> Exam)
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.id', ondelete="CASCADE"))
    exam = db.relationship(argument='Exam',
                           back_populates="sittings")
    # Sitting <-- Contains -->> Assessment
    assessments = db.relationship(argument='Assessment',
                                  back_populates="sitting",
                                  cascade="all, delete")

    # Student <<-- Reserves -->> Sitting (Association Table)
    bookers = db.relationship(argument='User',
                              secondary=reserves,
                              back_populates='reservations')

    def __init__(self):
        pass

    # Constraints
    # Start < End
    # Unique (Building, Room, Start, End)
    # Exams for 6 ECTS -> 1:30h, for 12 ECTS -> 3h
    def __repr__(self):
        return f'<Course: {self.id}>'

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
    evaluation_date = db.Column(db.DateTime, nullable=False,
                                default=datetime.datetime.utcnow())
    # Default 10 days from evaluation date, after which the exam expires
    expiry_acceptance_date = db.Column(db.DateTime, nullable=False,
                                       default=(datetime.datetime.utcnow() + datetime.timedelta(days=10)))
    # Modified by student when they accept it
    # NULL -> failed, True -> accepted, False -> rejected/expired
    accepted = db.Column(db.Boolean, nullable=True, default=None)
    acceptance_date = db.Column(db.DateTime, nullable=True, default=None)

    # Relationships
    # Assessment <<-- RefersTo --> Sitting (FK to Assessment)
    sitting_id = db.Column(db.Integer,
                           db.ForeignKey('sitting.id', ondelete="CASCADE"),
                           nullable=False)
    sitting = db.relationship(argument='Sitting',
                              back_populates="assessments")
    # Assessment <<-- AcceptedBy --> Student (If the reservation was made)
    student_id = db.Column(db.Integer,
                           db.ForeignKey('user.id', ondelete="CASCADE"),
                           nullable=False)
    student = db.relationship(argument='User',
                              back_populates='evaluations')

    def __init__(self, data):
        """
        Constructor

        Callable from a professor, who can only grade it. It may be created only if a student
        has made a reservation for the sitting_id.

        :param data: dictionary with 'grade'
        """
        self.grade = data.get('grade')
        if self.grade < 18:
            self.valid = False
        else:
            self.valid = True
        pass

    # @staticmethod
    # def load(assessment_id):
    #     return db.session.select(Assessment).filter_by(Assessment.id == assessment_id)
    #
    # def to_dict(self):
    #     data = {
    #         'id': self.id,
    #         'grade': self.grade,
    #         'valid': self.valid,
    #         'evaluation_date': self.evaluation_date,
    #         'expiry_acceptance_date': self.expiry_acceptance_date,
    #         'accepted': self.accepted,
    #         'acceptance_date': self.acceptance_date,
    #         'sitting_id': self.sitting_id,
    #         'student_id': self.student_id
    #     }
    #     return data
    #
    # def __repr__(self):
    #     return f'<Assessment: {self.id}>'

    # Assessment is created by professor, it refers to a sitting and a student
    # Assessment is updated by student, they can accept/refuse

    pass
