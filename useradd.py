from os import environ
from hashlib import sha512
from secrets import token_bytes
from datetime import datetime
from typing import Optional

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models import User


def get_session():
    engine = create_engine(environ['SQLALCHEMY_DATABASE_URI'])
    factory = sessionmaker(bind=engine)
    return factory


def main(email: Optional[str] = None):
    if email is None:
        email = input("email=")

    password = token_bytes(16).hex()

    user = User()
    user.email = email.strip()
    user.password = sha512(password.encode()).hexdigest()
    user.created_at = datetime.now()

    session = get_session()()
    session.add(user)
    session.commit()

    print(f"password={password}")


if __name__ == "__main__":
    load_dotenv()
    main()
