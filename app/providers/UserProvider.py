from .data.models import User


class UserProvider:

    def __init__(self, data):
    pass


class BoardProvider(UserProvider):
    pass


class ProfessorProvider(UserProvider):
    pass


class StudentProvider(UserProvider):
    pass
