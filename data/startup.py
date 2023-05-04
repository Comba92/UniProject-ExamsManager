"""
Start up module which focuses on creating the models and then filling the tables
with dummy data so that the application does not appear empty from the start.

"""
import datetime
from sqlalchemy import text
from flask_sqlalchemy.session import Session
from faker import Faker
from faker.providers import person, address, profile, ssn, phone_number
import bcrypt
from data.models import User


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

    for elem in range(1, count):
        # Initialize Seed
        fake = Faker()
        Faker.seed(894 + elem * 29)
        # Parameters
        person = profile.Provider(fake).profile()
        first_name = person.get('name').split()[0]
        last_name = person.get('name').split()[1]
        # Students have some numbers in their email
        soc_sec_num = person.get('ssn')
        if role == "Student":
            email = soc_sec_num.replace("-", "") + mail_suffix
        else:
            email = first_name + last_name + mail_suffix

        # Data
        data = {
            'role': role,
            'email': email,
            'password_hash': bcrypt.hashpw(soc_sec_num.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            'first_name': person.get('name').split()[0],
            'last_name': person.get('name').split()[1],
            'birth_day': fake.date_between(start_date=start_date, end_date=end_date),
            'birth_address': person.get('residence'),
            'address': person.get('address'),
            'ssn': soc_sec_num,
            'phone_number': phone_number.Provider(fake).phone_number()
        }
        users.append(data)
        elem += 25
    return users


def insert_random_users(db):
    # Insert without checking content
    boards = generate_user_data(count=10, role="Board", mail_suffix="@board.uni.it", min_age=50)
    professors = generate_user_data(count=10, role="Professor", mail_suffix="@prof.uni.it", min_age=30)
    students = generate_user_data(count=10, role="Student", mail_suffix="@stud.uni.it", max_age=30)

    for b in boards:
        with Session(db.engines) as db_session:
            new_board = User(b)
            db_session.add(new_board)
            db_session.commit()
    for p in professors:
        with Session(db.engines) as db_session:
            new_prof = User(p)
            db_session.add(new_prof)
            db_session.commit()
    for s in students:
        with Session(db.engines) as db_session:
            new_stud = User(s)
            db_session.add(new_stud)
            db_session.commit()
    pass


def generate_courses(db, count: int):
    pass


def generate_programs(db):
    pass


def insert_dummy_data(db):
    """
    Inserts dummy data inside the db, assuming the tables are created
    """
    # Data generation
    insert_random_users(db)
    pass


if __name__ == '__main__':
    # u = generate_user_data(count=10, role="Board", mail_suffix="@board.uni.it", min_age=50)
    # for i in u:
    #     print(i)
    # 
    # u = generate_user_data(count=30, role="Professor", mail_suffix="@prof.uni.it", min_age=30)
    # for i in u:
    #     print(i)
    # 
    # u = generate_user_data(count=150, role="Student", mail_suffix="@stud.uni.it", max_age=30)
    # for i in u:
    #     print(i)
    insert_random_users(db)
    pass
