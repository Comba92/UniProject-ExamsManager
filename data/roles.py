"""Module defining roles and privileges"""
from sqlalchemy import text
from config import VALID_USERS

# https://tableplus.com/blog/2018/04/postgresql-how-to-grant-access-to-users.html
# https://www.postgresql.org/docs/current/ddl-priv.html#:~:text=PostgreSQL%20grants%20privileges%20on%20some,%2C%20tablespaces%2C%20or%20configuration%20parameters.
# https://stackoverflow.com/questions/22288581/managing-user-privileges-in-sqlalchemy


def drop_role(user, session):
    """
    Drops ROLE associated with user variable inside the postgres database. Be aware
    that role with more privileges, might be at risk when their parent ROLE is dropped.
    :param: user is either "listener", "premium", "creator", "admin"
    """
    if role_exists(user=user, session=session):
        session.execute(text(
            "DROP OWNED BY {0};".format(user)
        ))
        session.execute(text(
            "DROP ROLE {0};".format(user)
        ))
    pass


def create_role_listener(session):
    session.execute(text(
        "CREATE ROLE listener WITH\n"
        "\tLOGIN\n"
        "\tNOSUPERUSER\n"
        "\tNOCREATEDB\n"
        "\tNOCREATEROLE\n"
        "\tNOINHERIT\n"
        "\tNOREPLICATION\n"
        "\tCONNECTION LIMIT -1\n"
        "\tENCRYPTED PASSWORD '{0}';".format(VALID_USERS["listener"])))
    set_listener_privileges(session)
    pass


def set_listener_privileges(session):
    """
    Normal listener can SELECT public active users, non-premium songs and song collections.
    They can INSERT, UPDATE, DELETE playlists, follows, likes
    """
    session.execute(text(
        "GRANT CONNECT ON DATABASE spotichad TO listener;"
    ))
    session.execute(text(
        "GRANT USAGE ON SCHEMA public TO listener;"
    ))
    # See
    # Users that are not admin, Non-premium content, follows, likes ...
    session.execute(text(
        "GRANT SELECT ON "
        "non_premium_song_view, non_premium_album_view, non_premium_playlist_view, "
        "public_users_view, creator_view, group_view, artist_view, soloist_view, "
        "follows, likes_song, likes_song_collection, features, "
        "genre, contains, likes_song, likes_song_collection, top_followed_creator_view, "
        "top_followed_view, non_premium_top_song TO listener;"
    ))
    # Add or remove
    # profile, follow, likes, playlists
    session.execute(text(
        "GRANT INSERT, DELETE ON \"user\", contains, follows, likes_song, likes_song_collection, song_collection "
        "TO listener;"
    ))
    # Modify
    # playlists and personal info
    session.execute(text(
        "GRANT UPDATE ON \"user\", contains, song_collection TO listener;"
    ))
    pass


def create_role_premium(session):
    """Creates ROLE premium which inherits from listener"""
    session.execute(text(
        "CREATE ROLE premium WITH\n"
        "\tLOGIN\n"
        "\tNOSUPERUSER\n"
        "\tNOCREATEDB\n"
        "\tNOCREATEROLE\n"
        "\tINHERIT\n"
        "\tNOREPLICATION\n"
        "\tCONNECTION LIMIT -1\n"
        "\tENCRYPTED PASSWORD '{0}';".format(VALID_USERS["premium"])))
    set_premium_privileges(session)
    pass


def set_premium_privileges(session):
    session.execute(text(
        "GRANT listener to PREMIUM"
    ))
    session.execute(text(
        "GRANT SELECT ON preview_album_view, preview_playlist_view, preview_song_view, "
        "released_album_view, released_playlist_view, released_song_view "
        "TO premium;"
    ))
    pass


def create_role_creator(session):
    """Creates ROLE creator which inherits from premium"""
    session.execute(text(
        "CREATE ROLE creator WITH\n"
        "\tLOGIN\n"
        "\tNOSUPERUSER\n"
        "\tNOCREATEDB\n"
        "\tNOCREATEROLE\n"
        "\tINHERIT\n"
        "\tNOREPLICATION\n"
        "\tCONNECTION LIMIT -1\n"
        "\tENCRYPTED PASSWORD '{0}';".format(VALID_USERS["creator"])))
    set_creator_privileges(session)
    pass


def set_creator_privileges(session):
    session.execute(text(
        "GRANT premium to creator"
    ))
    session.execute(text(
        "GRANT SELECT ON song, song_collection "
        "TO creator;"
    ))
    session.execute(text(
        "GRANT INSERT, UPDATE, DELETE ON features, song, song_collection "
        "TO creator;"
    ))
    pass


def create_role_admin(session):
    """Creates ROLE admin which inherits from creator"""
    session.execute(text(
        "CREATE ROLE admin WITH\n"
        "\tLOGIN\n"
        "\tSUPERUSER\n"
        "\tNOCREATEDB\n"
        "\tNOCREATEROLE\n"
        "\tINHERIT\n"
        "\tNOREPLICATION\n"
        "\tBYPASSRLS\n"
        "\tCONNECTION LIMIT -1\n"
        "\tENCRYPTED PASSWORD '{0}';".format(VALID_USERS["admin"])))
    set_admin_privileges(session)
    pass


def set_admin_privileges(session):
    session.execute(text(
        "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO admin;"
    ))
    pass


def drop_all_roles(session):
    for i in VALID_USERS:
        if i == "postgres":
            continue
        drop_role(session=session, user=i)
    pass


def check_privileges(session, user, grantee="grantee", table_schema="table_schema", table_name="table_name"):
    if user in VALID_USERS:
        result = session.execute(text(
            "SELECT grantor, {0}, {1}, {2}, privilege_type \n".format(grantee, table_schema, table_name) +
            "FROM information_schema.table_privileges \n"
            "WHERE grantee = '{0}';".format(user)
        ))
        print("User: " + user + " has the following privileges")
        for item in result:
            print(item.privilege_type + " privilege on " + item.table_name)
    else:
        raise Exception("User not found: " + user)
    pass


def check_all_privileges(session):
    for i in VALID_USERS:
        if i == "postgres":
            continue
        check_privileges(session=session, user=i)
    pass


def role_exists(session, user):
    if user in VALID_USERS:
        result = session.execute(text(
            "SELECT pg_user.usename \n"
            "FROM pg_catalog.pg_user \n"
            "WHERE pg_user.usename = '{0}';".format(user)
        ))
        for row in result:
            if user in row[0]:
                return True
    return False


def init_serverside_roles(session):
    """
    Initialize server-side ROLEs for listener, premium, creator, admin. creator inherits from premium,
    which in turn inherits from listener. It drops the roles upon creation for integrity purposes.
    :param session: Session object with privileges for creating new roles on the database
    """
    drop_all_roles(session)
    create_role_listener(session)
    create_role_premium(session)
    create_role_creator(session)
    create_role_admin(session)
    pass