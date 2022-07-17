from os import environ

key = environ['JWT_SECRET']
algorithms = ['HS256']

# registered claim #
iss = environ['ISS']
