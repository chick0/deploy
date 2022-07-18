from hashlib import sha512
from datetime import datetime

from sql import get_session
from sql.models import User
from utils.uuid import get_uuid


def main() -> None:
    """
    Create user

    :return:
    """
    session = get_session()

    user = User()
    user.uuid = get_uuid()
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
