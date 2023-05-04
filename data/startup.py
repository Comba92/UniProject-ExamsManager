"""
Start up module which focuses on creating the models and then filling the tables
with dummy data so that the application does not appear empty from the start.

"""
import datetime
from sqlalchemy import text
from flask_sqlalchemy.session import Session
from faker import Faker
from faker.providers import person, address, profile, ssn, phone_number
from bcrypt import hashpw, gensalt


def return_sex(sex_string):
    """
    Util method to decode binary-gender
    :param sex_string: either 'M' or 'F'
    :return: either 'Male' or 'Female'
    """
    if sex_string == 'M':
        return 'Male'
    else:
        return 'Female'


def return_dates_range(min_age=18, max_age=70):
    try:
        if isinstance(min_age, int) and isinstance(max_age, int):
            min_date = datetime.date(year=int(datetime.date.today().year) - min_age,
                                     month=int(datetime.date.today().month),
                                     day=int(datetime.date.today().day))
            max_date = datetime.date(year=int(datetime.date.today().year) - max_age,
                                     month=int(datetime.date.today().month),
                                     day=int(datetime.date.today().day))
            return min_date, max_date
    except:
        raise TypeError("min_age and max_age must be integers, received instead: \n"
                        "type(min_age) -> " + str(type(min_age)) + "\t type(max_age) ->" + str(type(max_age)))
    finally:
        # Returns default
        return_dates_range()
    pass


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
        first_name = person.Provider(fake).first_name()
        last_name = person.Provider(fake).last_name()
        # Students have some numbers in their email
        ssn = ssn.Provider(fake).ssn().replace("-", "")
        if role == "Student":
            email = ssn + mail_suffix
        else:
            email = first_name + last_name + mail_suffix

        # Data
        data = {
            'role': role,
            'email': email,
            'password_hash': str(hashpw(bytes(ssn), gensalt())),
            'first_name': first_name,
            'last_name': last_name,
            'birth_day': fake.date_between(start_date=start_date, end_date=end_date),
            'birth_address': address.Provider(fake).address(),
            'address': address.Provider(fake).address(),
            'ssn': ssn,
            'phone_number': phone_number.Provider(fake).phone_number()
        }
        users.append(data)
    return users


def insert_random_users(db):
    # Array of
    boards = generate_user_data(count=10, role="Board", mail_suffix="@board.uni.it", min_age=50)
    professors = generate_user_data(count=30, role="Professor", mail_suffix="@prof.uni.it", min_age=30)
    students = generate_user_data(count=150, role="Student", mail_suffix="@stud.uni.it", max_age=30)

    with Session(db.engines['postgres']) as db_session:
        for b in boards:
            new_board = UserProvider.from_dict(b)
            db_session.add(new_board)
            db_session.commit()
        for p in professors:
            new_prof = UserProvider.from_dict(p)
            db_session.add(new_prof)
            db_session.commit()
        for s in students:
            new_stud = BoardProvider.from_dict(s)
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
    generate_roles(db)
    generate_genres(db)
    generate_admin(db)
    generate_users(db)
    generate_artists(db)
    generate_songs(db)
    generate_genres_playlists(db)
    generate_decade_playlists(db)
    generate_artist_playlists(db)
    generate_random_user_playlists(db)
    pass


if __name__ == '__main__':
    u = generate_user_data(count=10, role="Board", mail_suffix="@board.uni.it", min_age=50)
    for i in u:
        print(i)
    pass
