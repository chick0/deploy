from os import environ
from datetime import datetime
from datetime import timedelta

key = environ['JWT_SECRET']
algorithms = ['HS256']

# registered claim #
iss = environ['ISS']


def iat() -> int:
    """
    Get token issued time

    :return: (iat) issued at
    """
    return int(datetime.now().timestamp())


def exp() -> int:
    """
    Get token expiration time

    :return: (exp) expiration
    """
    return int((datetime.now() + timedelta(hours=3)).timestamp())
