"""
Start up module which focuses on creating the models and then filling the tables
with dummy data so that the application does not appear empty from the start.
"""
import pandas as pd
import datetime
from sqlalchemy import text
from flask_sqlalchemy.session import Session
from app.providers import UserProvider, CreatorProvider, SongProvider, SongCollectionProvider
from faker import Faker
from faker.providers import person, address, profile


def generate_board(db):
    pass


def generate_professors(db):
    pass


def generate_students(db):
    pass


def generate_courses(db):
    pass


def generate_programs(db):
    prog_dict = {
        "Computer Science": 1,
        "Civil Engineering": 2,
        "Medicine": 3,
    }
    pass


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


def generate_users(db):
    """
    Random users generator using faker providers and local sqlalchemy models,
    which adds instances of users inside the local db
    """
    start_date = datetime.date(year=1940, month=1, day=1)
    end_date = datetime.date(year=int(datetime.date.today().year) - 18,
                             month=int(datetime.date.today().month),
                             day=int(datetime.date.today().day))
    # sub = None
    # end_sub = None

    for u in range(1, 100):
        fake = Faker()
        Faker.seed(894 + u * 29)
        username = person.Provider(fake).language_name() + str(person.Provider(fake).random_int())
        # prem = person.Provider(fake).random_int(min=0, max=1)
        # prem_dates = return_premium(prem, fake)

        with Session(db.engines['admin']) as db_session:
            sample_user = UserProvider.UserProvider.create_profile(
                data={
                    'name': profile.Provider(fake).simple_profile().get('username'),
                    'email': profile.Provider(fake).simple_profile().get('mail'),
                    'first_name': profile.Provider(fake).simple_profile().get('name').split()[0],
                    'last_name': profile.Provider(fake).simple_profile().get('name').split()[1],
                    'region': address.Provider(fake).country(),
                    'password': username,
                    'birthday': fake.date_between(start_date=start_date, end_date=end_date),
                    'gender': return_sex(profile.Provider(fake).simple_profile().get('sex')),
                    'bio': "I love spotichad"
                }
            )
            db_session.add(sample_user)
            db_session.commit()
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
    pass
