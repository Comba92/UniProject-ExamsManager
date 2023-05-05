"""
Module defining roles and privileges. The module is only tested for postgres.

"""
from sqlalchemy import text
from config import VALID_USERS, PRIVILEGES


# https://tableplus.com/blog/2018/04/postgresql-how-to-grant-access-to-users.html
# https://www.postgresql.org/docs/current/ddl-priv.html#:~:text=PostgreSQL%20grants%20privileges%20on%20some,%2C%20tablespaces%2C%20or%20configuration%20parameters.
# https://stackoverflow.com/questions/22288581/managing-user-privileges-in-sqlalchemy

def is_super_user_session(session) -> bool:
    """
    Checks whether the current session is a super_user session

    """
    if session.bind is None or session.bind == "postgres":
        return True
    return False


def role_exists(session, role) -> bool:
    """
    Returns whether a role exists in the database associated with the current session

    """
    if role in VALID_USERS:
        result = session.execute(text(
            "SELECT pg_user.usename \n"
            "FROM pg_catalog.pg_user \n"
            "WHERE pg_user.usename = '{0}';".format(role)
        ))
        for row in result:
            if role in row[0]:
                return True
        return False
    else:
        print("Role " + role + " does not exist")
    return False


def grant_connection(session, role: str, database="postgres", schema="public"):
    """
    Script that grants connection privilege to a particular role to a database associated with the current session.

    """
    if is_super_user_session(session) and role_exists(session, role):
        session.execute(text(
            "GRANT CONNECT ON DATABASE " + database + " TO " + role + ";"
        ))
        session.execute(text(
            "GRANT USAGE ON SCHEMA " + schema + " TO " + role + ";"
        ))
    pass


def drop_role(session, role):
    """
    Drops ROLE associated with role variable inside the postgres database. Be aware
    that role with more privileges, might be at risk when their parent ROLE is dropped.
    :param: user is VALID_USERS. It only works with postgres
    """
    if role_exists(session=session, role=role):
        session.execute(text(
            "DROP OWNED BY {0};".format(role)
        ))
        session.execute(text(
            "DROP ROLE {0};".format(role)
        ))
    pass


def drop_all_roles(session):
    for i in VALID_USERS:
        if i == "postgres":
            continue
        drop_role(session=session, role=i)
    pass


def create_role(session, role, superuser=False):
    statement = ""
    if role in VALID_USERS.keys():
        if superuser:
            statement = "CREATE ROLE " + role + " WITH\n" \
                                                " \tLOGIN\n " \
                                                "\tSUPERUSER\n" \
                                                "\tNOCREATEDB\n" \
                                                "\tNOCREATEROLE\n" \
                                                "\tNOINHERIT\n" \
                                                "\tNOREPLICATION\n" \
                                                "\tCONNECTION LIMIT -1\n" \
                                                "\tENCRYPTED PASSWORD '{0}';".format(VALID_USERS.get(role))
        else:
            statement = "CREATE ROLE " + role + " WITH\n" \
                                                "\tLOGIN\n" \
                                                "\tNOSUPERUSER\n" \
                                                "\tNOCREATEDB\n" \
                                                "\tNOCREATEROLE\n" \
                                                "\tNOINHERIT\n" \
                                                "\tNOREPLICATION\n" \
                                                "\tCONNECTION LIMIT -1\n" \
                                                "\tENCRYPTED PASSWORD '{0}';".format(VALID_USERS.get(role))
        session.execute(text(statement))
        grant_connection(session, role)
    else:
        raise PermissionError("The only valid roles are described in config.py -> VALID_USERS")
    pass


def grant_privilege(session, role: str, privilege: str, tables=None):
    # Check session is super
    # Check role exists
    # Check privilege exists
    # Check tables exist

    # Define Statement
    if privilege == "ALL":
        statement = "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO " + role + ";"
    else:
        statement = "GRANT " + privilege + " ON "
        # Add commas until the last table has been reached.
        for t in tables:
            statement += "\"" + t + "\"" + " ,"
        # Remove last comma
        statement = statement.rstrip(statement[-1])
        # Assign to role
        statement += "TO " + role + ";"
    session.execute(text(statement))
    pass


def set_role_privileges(super_user_session, role, database='postgres', schema='public',
                        select=None, insert=None, delete=None, update=None):
    pass


def check_privileges(session, role, grantee="grantee", table_schema="table_schema", table_name="table_name"):
    if role in VALID_USERS:
        result = session.execute(text(
            "SELECT grantor, {0}, {1}, {2}, privilege_type \n".format(grantee, table_schema, table_name) +
            "FROM information_schema.table_privileges \n"
            "WHERE grantee = '{0}';".format(role)
        ))
        print("User: " + role + " has the following privileges")
        for item in result:
            print(item.privilege_type + " privilege on " + item.table_name)
    else:
        raise Exception("User not found: " + role)
    pass


def check_all_privileges(session):
    for i in VALID_USERS:
        if i == "postgres":
            continue
        check_privileges(session=session, role=i)
    pass


def init_serverside_roles(session, drop_first=True):
    """
    Initialize server-side ROLEs. It can drop the roles upon creation for integrity purposes.
    :param drop_first:
    :param session: Session object with privileges for creating new roles on the database
    """
    if drop_first is True:
        drop_all_roles(session)
    create_role(session, "admin", superuser=False)
    grant_connection(session, "admin")
    grant_privilege(session, "admin", "SELECT", ["user"])
    pass

