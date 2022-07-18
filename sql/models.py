from dataclasses import dataclass

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import SmallInteger
from sqlalchemy import Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


@dataclass
class User(Base):
    """
    Database models for check login and auth
    """
    __tablename__ = "user"

    uuid = Column(
        String(36),
        unique=True,
        primary_key=False,
        nullable=False
    )

    email = Column(
        String(120),
        unique=True,
        primary_key=True,
        nullable=False
    )

    password = Column(
        String(128),
        nullable=False
    )

    created_at = Column(
        DateTime,
        nullable=False,
    )

    last_login_at = Column(
        DateTime,
        nullable=False,
    )


@dataclass
class Project(Base):
    """
    Database models for manage project
    """
    __tablename__ = "project"

    uuid = Column(
        String(36),
        unique=True,
        primary_key=True,
        nullable=False
    )

    title = Column(
        String(120),
        nullable=False
    )

    owner = Column(
        String(36),
        ForeignKey("user.uuid")
    )

    created_at = Column(
        DateTime,
        nullable=False,
    )

    deploy_at = Column(
        DateTime,
        nullable=True,
    )

    deploy_by = Column(
        String(36),
        ForeignKey("user.uuid")
    )

    # utils.type.ProjectType
    type = Column(
        SmallInteger,
        nullable=False,
    )

    # ignored in front project
    path = Column(
        String(255),
        nullable=True
    )


@dataclass
class DeployToken(Base):
    """
    Database models for check deploy token
    """
    __tablename__ = "deploy_token"

    uuid = Column(
        String(36),
        unique=True,
        primary_key=True,
        nullable=False
    )

    project = Column(
        String(36),
        ForeignKey("project.uuid")
    )

    create_by = Column(
        String(36),
        ForeignKey("user.uuid")
    )

    read = Column(
        Boolean,
        default=False
    )

    write = Column(
        Boolean,
        default=False
    )

    delete = Column(
        Boolean,
        default=False
    )
