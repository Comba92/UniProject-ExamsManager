"""
Start up module which focuses on creating the models and then filling the tables
with dummy data so that the application does not appear empty from the start.

"""
import datetime
from sqlalchemy import text, select
from faker import Faker
from faker.providers import profile, phone_number, job
import bcrypt
from data.models import User, Program, Course, Exam, Sitting, Role
from werkzeug.security import generate_password_hash

ARCHAEOLOGY = ["Aerial archaeology", "Aviation archaeology", "Anthracology",
               "Archaeogeography", "Archaeological culture", "Archaeological theory",
               "Manuscriptology", "Maritime archaeology", "Media archaeology"]
HISTORY = ["African history", "American history", "Ancient history",
           "Asian history", "Economic history", "Political history",
           "Australian history", "Public history", "World history"]
LINGUISTICS = ["Applied linguistics", "Composition studies", "Computational linguistics",
               "Discourse analysis", "English studies", "Grammar",
               "Etymology", "Grammatology", "Historical linguistics"]
LITERATURE = ["Comics studies", "Comparative literature", "Creative writing",
              "English literature", "History of literature", "Medieval literature",
              "Ancient literature", "Post-colonial literature", "Post-modern literature"]
ECONOMICS = ["Agricultural economics", "Anarchist economics", "Applied economics",
             "Behavioural economics", "Bioeconomics", "Complexity economics",
             "Computational economics", "Consumer economics", "Development economics"]
POLITICALSCIENCE = ["American politics", "Canadian politics", "Civics",
                    "Comparative politics", "European studies", "Geopolitics",
                    "International relations", "International organizations", "Nationalism studies"]
PSYCHOLOGY = ["Abnormal psychology", "Applied psychology", "Biological psychology",
              "Clinical neuropsychology", "Clinical psychology", "Cognitive psychology",
              "Community psychology", "Comparative psychology", "Conservation psychology"]
BIOLOGY = ["Human anatomy", "Biochemistry", "Bioinformatics",
           "Biophysics", "Biotechnology", "Botany",
           "Cell biology", "Computational biology", "Cryobiology"]
CHEMISTRY = ["Petrochemistry", "Pharmacology", "Photochemistry",
             "Physical chemistry", "Physical organic chemistry", "Polymer chemistry",
             "Quantum chemistry", "Radiochemistry", "Sonochemistry"]
PHYSICS = ["Aerodynamics", "Applied physics", "Astrophysics",
           "Biophysics", "Computational physics", "Condensed matter physics",
           "Cryogenics", "Electricity", "Electromagnetism"]
COMPUTERSCIENCE = ["Data structures", "Computer architecture", "Computer graphics",
                   "Image processing", "Cloud computing", "Cryptography",
                   "Computational mathematics", "Wireless computing", "Computer communications "]
PROGRAMS = {
    "Archaeology": ARCHAEOLOGY,
    "History": HISTORY,
    "Linguistics and languages": LINGUISTICS,
    "Literature": LITERATURE,
    "Economics": ECONOMICS,
    "Political science": POLITICALSCIENCE,
    "Psychology": PSYCHOLOGY,
    "Biology": BIOLOGY,
    "Chemistry": CHEMISTRY,
    "Physics": PHYSICS,
    "Computer science": COMPUTERSCIENCE,
}


def return_dates_range(min_age=18, max_age=70):
    if isinstance(min_age, int) and isinstance(max_age, int):
        min_date = datetime.date(year=int(datetime.date.today().year) - min_age,
                                 month=int(datetime.date.today().month),
                                 day=int(datetime.date.today().day))
        max_date = datetime.date(year=int(datetime.date.today().year) - max_age,
                                 month=int(datetime.date.today().month),
                                 day=int(datetime.date.today().day))
        return min_date, max_date
    else:
        return_dates_range()


def generate_user_data(count: int, role: str, mail_suffix: str, min_age=18, max_age=70):
    """
    Random users' generator using faker providers and local sqlalchemy models,
    which adds instances of users inside the local db
    """
    # Dictionary Array
    users = []
    # Fix the range of age
    end_date, start_date = return_dates_range(min_age=min_age, max_age=max_age)

    for elem in range(0, count):
        # Initialize Seed
        fake = Faker()
        Faker.seed(894 + elem * 29)
        # Parameters
        new_person = profile.Provider(fake).profile()
        first_name = new_person.get('name').split()[0]
        last_name = new_person.get('name').split()[1]
        # Students have some numbers in their email
        soc_sec_num = new_person.get('ssn').replace("-", "")
        if role == "Student":
            email = soc_sec_num + mail_suffix
        else:
            email = first_name + last_name + mail_suffix

        # Data
        data = {
            'role': role,
            'email': email,
            'password_hash': generate_password_hash(password=soc_sec_num, salt_length=8),
            'first_name': new_person.get('name').split()[0],
            'last_name': new_person.get('name').split()[1],
            'birth_day': fake.date_between(start_date=start_date, end_date=end_date),
            'birth_address': new_person.get('residence').replace("\n", ""),
            'address': new_person.get('address').replace("\n", ""),
            'ssn': soc_sec_num,
            'phone_number': phone_number.Provider(fake).phone_number().replace("-", "")
        }
        users.append(data)
        elem += 25
    return users


def insert_generated_roles(db):
    ROLES = ["login", "student", "professor", "board"]
    for r in ROLES:
        role = Role(data={"name": r})
        db.session.add(role)
        db.session.commit()
    pass


def insert_generated_users(db):
    boards = generate_user_data(count=10, role="Board", mail_suffix="@board.uni.it", min_age=50)
    professors = generate_user_data(count=10, role="Professor", mail_suffix="@prof.uni.it", min_age=30)
    students = generate_user_data(count=10, role="Student", mail_suffix="@stud.uni.it", max_age=30)

    student_role = db.session.scalars(select(Role).where(Role.name == "student")).all()[0]
    professor_role = db.session.scalars(select(Role).where(Role.name == "professor")).all()[0]
    board_role = db.session.scalars(select(Role).where(Role.name == "board")).all()[0]
    login_role = db.session.scalars(select(Role).where(Role.name == "login")).all()[0]

    for b in boards:
        new_board = User(b)
        login_role.users.append(new_board)
        board_role.users.append(new_board)
        db.session.add(new_board)
        db.session.commit()
    for p in professors:
        new_prof = User(p)
        login_role.users.append(new_prof)
        professor_role.users.append(new_prof)
        db.session.add(new_prof)
        db.session.commit()
    for s in students:
        new_stud = User(s)
        login_role.users.append(new_stud)
        student_role.users.append(new_stud)
        db.session.add(new_stud)
        db.session.commit()
    pass


def insert_generated_programs(db):
    for p in PROGRAMS:
        # Create new program
        new_program = Program(data={
            'name': p,
            'credits': 180,
            'start': datetime.datetime(year=2023, month=9, day=1),
            'end': datetime.datetime(year=2026, month=6, day=1)
        })
        db.session.add(new_program)
        courses = PROGRAMS.get(p)
        for c in courses:
            # Add the courses to the program after creation
            new_course = Course(data={'name': c,
                                      'credits': 6,
                                      'semester': 1,
                                      'module': 1})
            new_program.courses.append(new_course)
            db.session.add(new_course)
            db.session.commit()
    pass


def delete_all(db, instances):
    """
    Deletes all instances from the database

    :param db: engine or SQLAlchemy Object
    :param instances: array of table instances
    :return: None
    """
    for i in instances:
        db.session.delete(i)
        db.session.commit()
    pass


def delete_roles(db):
    roles = db.session.scalars(select(Role)).all()
    delete_all(db, roles)
    pass


def delete_users(db):
    """
    Deletes all users from the database

    :param db: engine or SQLAlchemy Object
    :return: None
    """
    users = db.session.scalars(select(User)).all()
    delete_all(db, users)
    pass


def delete_programs(db):
    """
    Deletes all board from the database

    :param db: engine or SQLAlchemy Object
    :return: None
    """
    programs = db.session.scalars(select(Program)).all()
    delete_all(db, programs)
    pass


def delete_courses(db):
    """
    Deletes all courses from the database

    :param db: engine or SQLAlchemy Object
    :return: None
    """
    courses = db.session.scalars(select(Course)).all()
    delete_all(db, courses)
    pass


def insert_dummy_data(db, drop_first=True):
    """
    Inserts dummy data inside the db, assuming the tables are created
    """
    # Data generation
    if drop_first:
        delete_roles(db)
        delete_users(db)
        delete_programs(db)
        delete_courses(db)
    insert_generated_roles(db)
    insert_generated_users(db)
    insert_generated_programs(db)
    pass


if __name__ == '__main__':
    insert_generated_programs(db=None)
    pass
