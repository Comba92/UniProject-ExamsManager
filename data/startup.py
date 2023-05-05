"""
Start up module which focuses on creating the models and then filling the tables
with dummy data so that the application does not appear empty from the start.

"""
import datetime
from sqlalchemy import text
from faker import Faker
from faker.providers import profile, phone_number, job
import bcrypt
from data.models import User, Program, Course, Exam, Sitting
from werkzeug.security import generate_password_hash

ARCHAEOLOGY = ["Aerial archaeology", "Aviation archaeology", "Anthracology",
               "Archaeogeography", "Archaeological culture", "Archaeological theory"
                                                             "Manuscriptology", "Maritime archaeology",
               "Media archaeology"]
HISTORY = []
LINGUISTICS = []
LITERATURE = []
ECONOMICS = []
POLITICALSCIENCE = []
PSYCHOLOGY = []
BIOLOGY = []
CHEMISTRY = []
PHYSICS = []
COMPUTERSCIENCE = []

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


def insert_generated_users(db):
    # Insert without checking content
    boards = generate_user_data(count=10, role="Board", mail_suffix="@board.uni.it", min_age=50)
    professors = generate_user_data(count=10, role="Professor", mail_suffix="@prof.uni.it", min_age=30)
    students = generate_user_data(count=10, role="Student", mail_suffix="@stud.uni.it", max_age=30)

    for b in boards:
        new_board = User(b)
        db.session.add(new_board)
        db.session.commit()
    for p in professors:
        new_prof = User(p)
        db.session.add(new_prof)
        db.session.commit()
    for s in students:
        new_stud = User(s)
        db.session.add(new_stud)
        db.session.commit()
    pass


def generate_programs():
    for program in PROGRAMS:
        courses = PROGRAMS.get(program)
        print(program, courses)

    # Generate courses
    # Add courses to program
    # commit
    pass


def insert_dummy_data(db):
    """
    Inserts dummy data inside the db, assuming the tables are created
    """
    # Data generation
    insert_generated_users(db)
    pass


if __name__ == '__main__':
    generate_programs()
    pass
