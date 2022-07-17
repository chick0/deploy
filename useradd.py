from uuid import uuid4
from hashlib import sha512
from datetime import datetime

from sql import get_session
from sql.models import User


def main():
    session = get_session()

    user = User()
    user.uuid = uuid4().__str__()
    user.email = input("email=")
    user.password = sha512(input("password=").encode()).hexdigest()
    user.created_at = datetime.now()
    user.last_login_at = datetime.now()

    session.add(user)
    session.commit()
    session.close()
    print("-> user created")


if __name__ == "__main__":
    main()
