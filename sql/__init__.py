from os import environ

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from dotenv import load_dotenv

if 'SQLALCHEMY_DATABASE_URI' not in environ:
    load_dotenv()

engine = create_engine(
    url=environ['SQLALCHEMY_DATABASE_URI'],
    pool_size=10,
    max_overflow=20
)

session_factory = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


def get_session() -> Session:
    """
    Get sqlalchemy session

    :return: sqlalchemy session
    """
    return session_factory()
