"""
Start up module which focuses on creating the models and then filling the tables
with dummy data so that the application does not appear empty from the start.
"""
import pandas as pd
import datetime
from sqlalchemy import text
from flask_sqlalchemy.session import Session
from app.providers import UserProvider, CreatorProvider, SongProvider, SongCollectionProvider
from app.providers.UserProvider import Role
from models import Genre
from config import get_from_env
from faker import Faker
from faker.providers import person, address, profile

DF = pd.read_csv(get_from_env("SONGS"))


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


# def return_premium(prem, fake_inst):
#     """
#     Util method to for premium subscriptions
#     :param prem: a boolean indicating whether the user is a premium user
#     :param fake_inst: instance of faker object with initialized seed
#     :return: A list with two elements: premium subscription datetime, end of premium subscription datetime
#     """
#     sub = None
#     end_sub = None
#     if prem:
#         sub = datetime.datetime.now()
#         end_sub = fake_inst.date_time_between(start_date=(datetime.date.today() + datetime.timedelta(days=1)),
#                                               end_date='+30ys')
#     return [sub, end_sub]


def generate_roles(db):
    role = {'listener': 16,
            'premium': 32,
            'creator': 64,
            'admin': 128,
            }
    for k, v in role.items():
        with Session(db.engines['postgres']) as db_session:
            if v > 16:
                db_session.add(Role(name=k, default=False, permission=v))
            else:
                db_session.add(Role(name=k, default=True, permission=v))
            db_session.commit()
    pass


def generate_genres(db):
    """
    Random genres generator, which adds instances of songs inside the local db
    """
    genres = DF.iloc[:, 4].unique().tolist()

    with Session(db.engines['postgres']) as db_session:
        db_session.add(Genre(
            identifier=0,
            name="Unknown"
        ))
        for g in genres:
            sample_genre = Genre(
                name=g.capitalize()
            )
            db_session.add(sample_genre)
            db_session.commit()
    pass


def generate_admin(db):
    """
    Adds superuser for administration purposes
    """
    admin = UserProvider.AdminProvider()
    admin.create_profile(data={
                    'name': profile.Provider(fake).simple_profile().get('username'),
                    'email': profile.Provider(fake).simple_profile().get('mail'),
                    'first_name': profile.Provider(fake).simple_profile().get('name').split()[0],
                    'last_name': profile.Provider(fake).simple_profile().get('name').split()[1],
                    'region': address.Provider(fake).country(),
                    'password': username,
                    'birthday': fake.date_between(start_date=start_date, end_date=end_date),
                    'gender': return_sex(profile.Provider(fake).simple_profile().get('sex')),
                    'bio': "I love spotichad"
                })
    pass


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


def users_subscribe(db):
    pass

def generate_artists(db):
    """
    Random artists generator using faker providers and local sqlalchemy models,
    which adds instances of artists inside the local db
    """
    artists = DF.iloc[:, 3].unique()

    fake = Faker()
    Faker.seed(4454)
    start_date = datetime.date(year=1940, month=1, day=1)
    end_date = datetime.date(year=int(datetime.date.today().year) - 18,
                             month=int(datetime.date.today().month),
                             day=int(datetime.date.today().day))
    for a in artists:
        with SESSIONS['creator'] as db_session:
            sample_artist = Artist(
                name=a,
                email=(a.replace(" ", "") + "@spotichad.com"),
                password=a,
                birthday=fake.date_between(start_date=start_date, end_date=end_date),
                in_prod=True
            )
            db_session.add(sample_artist)
            db_session.commit()
    pass


def artists_add_songs(db):
    pass


def generate_songs(db):
    """
    Random songs generator using faker providers and local sqlalchemy models,
    which adds instances of songs inside the local db
    """
    mysongs = DF
    fake = Faker()
    for i in range(len(mysongs)):
        if len(mysongs.iloc[i, 12]) > 3:
            continue

        Faker.seed(368 + i * 9)
        with SESSIONS['artist'] as db_session:
            sample_song = Song(
                session=db_session,
                name=mysongs.iloc[i, 2],
                artist_username=mysongs.iloc[i, 3],
                genre=mysongs.iloc[i, 4].capitalize(),
                bpm=int(mysongs.iloc[i, 6]),
                energy=int(mysongs.iloc[i, 7]),
                danceability=int(mysongs.iloc[i, 8]),
                loudness=int(mysongs.iloc[i, 9]),
                valence=int(mysongs.iloc[i, 11]),
                length=int(mysongs.iloc[i, 12]),
                acousticness=int(mysongs.iloc[i, 13]),
                speechiness=int(mysongs.iloc[i, 14]),
                year=int(mysongs.iloc[i, 5]),
                date_re=datetime.datetime(year=mysongs.iloc[i, 5], month=1, day=1),
                date_cre=datetime.datetime.today(),
                date_upd=datetime.datetime.today(),
                is_released=bool((person.Provider(fake).random_int(min=0, max=100) % 2)),
                is_premium=bool(person.Provider(fake).random_int(min=0, max=1)),
                stream=person.Provider(fake).random_int(min=100, max=1000),
                in_prod=True
            )
            db_session.add(sample_song)
            db_session.commit()
    pass


def set_playlist_songs(mysession, playlist_id, songs):
    if songs is not None:
        for i in songs:
            mysession.execute(
                text("INSERT INTO playlist_contains_song_assoc(playlist_id, song_id)"
                     "VALUES ({0},{1})".format(playlist_id, i))
            )
    pass


def generate_decade_playlists(db):
    """
    Generates system-made playlists based on the decade of release
    :param db_session: A sqlalchemy.orm.session object with postgres privileges
    """

    fake = Faker()
    for decade in range(1960, 2020, 10):
        Faker.seed(48 + decade * 9)

        with SESSIONS['listener'] as db_session:
            sample_playlist = Playlist(
                session=db_session,
                name=(str(decade) + "s Top Hits"),
                owner_id=1,
                date_cre=datetime.datetime.today(),
                date_upd=datetime.datetime.today(),
                date_re=datetime.datetime.today(),
                is_released=True,
                is_premium=False,
                stream=person.Provider(fake).random_int(min=100, max=1000),
                in_prod=True
            )
            db_session.add(sample_playlist)
            db_session.commit()

            songs = []
            result = db_session.query(Song.id).filter(Song.year < decade).order_by(Song.stream_quantity).limit(15)
            for row in result:
                songs.append(row.id)

            set_playlist_songs(mysession=db_session, playlist_id=sample_playlist.id, songs=songs)
    pass


def generate_genres_playlists(db):
    """
    Generates system-made playlists based on the genres
    """
    fake = Faker()
    with SESSIONS['listener'] as db_session:
        result = db_session.query(Genre.id, Genre.name)
        for row in result:
            Faker.seed(788 + row.id * 2)
            sample_playlist = Playlist(
                session=db_session,
                name=(row.name + " Classics"),
                owner_id=1,
                date_cre=datetime.datetime.today(),
                date_upd=datetime.datetime.today(),
                date_re=datetime.datetime.today(),
                is_released=True,
                is_premium=False,
                stream=person.Provider(fake).random_int(min=100, max=1000),
                in_prod=True,
                main_genre_id=row.id
            )
            db_session.add(sample_playlist)
            db_session.commit()

            songs_by_genre = db_session.query(Song.id).filter(Song.id == row.id).limit(20)
            songs = []
            for item in songs_by_genre:
                songs.append(row.id)
            set_playlist_songs(mysession=db_session, playlist_id=sample_playlist.id, songs=songs)
    pass


def generate_artist_playlists(db):
    """
    Generates system-made playlists based on artist
    :param db_session: A sqlalchemy.orm.session object with postgres privileges
    """
    fake = Faker()
    with SESSIONS['listener'] as db_session:
        result = db_session.query(Artist.id, Artist.name)
        for row in result:
            Faker.seed(788 + row.id * 2)
            sample_playlist = Playlist(
                session=db_session,
                name=(row.name + "'s Unforgettable Records"),
                owner_id=1,
                date_cre=datetime.datetime.today(),
                date_upd=datetime.datetime.today(),
                date_re=datetime.datetime.today(),
                is_released=True,
                is_premium=False,
                stream=person.Provider(fake).random_int(min=100, max=1000),
                in_prod=True,
            )
            db_session.add(sample_playlist)
            db_session.commit()

            songs_by_artists = db_session.query(Song.id).filter(Song.artist_id == row.id).limit(10)
            songs = []
            for item in songs_by_artists:
                songs.append(row.id)
            set_playlist_songs(mysession=db_session, playlist_id=sample_playlist.id, songs=songs)

    pass


def generate_random_user_playlists(db):
    """
    Generates user-made playlists randomly
    """
    fake = Faker()
    with SESSIONS['listener'] as db_session:
        users = db_session.query(User.id, User.name).filter(User.id > 1)
        for row in users:
            Faker.seed(788 + row.id * 2)
            sample_playlist = Playlist(
                session=db_session,
                name=(row.name + "'s Favorite Songs"),
                owner_id=row.id,
                date_cre=datetime.datetime.today(),
                date_upd=datetime.datetime.today(),
                date_re=datetime.datetime.today(),
                is_released=True,
                is_premium=False,
                stream=person.Provider(fake).random_int(min=100, max=1000),
                in_prod=True,
            )
            db_session.add(sample_playlist)
            db_session.commit()

            songs = []
            random_songs = db_session.query(Song.id).filter(Song.id > person.Provider(fake).random_int(min=1,
                                                                                                       max=1900)).limit(
                15)
            for item in random_songs:
                if item.id in songs:
                    continue
                songs.append(item.id)
            set_playlist_songs(mysession=db_session, playlist_id=sample_playlist.id, songs=songs)
    pass


def simulate_actions(db):
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