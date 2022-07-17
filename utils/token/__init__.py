from os import environ
from datetime import datetime
from datetime import timedelta

key = environ['JWT_SECRET']
algorithms = ['HS256']

# registered claim #
iss = environ['ISS']
iat = lambda: datetime.now().timestamp()
exp = lambda: (datetime.now() + timedelta(hours=3)).timestamp()
