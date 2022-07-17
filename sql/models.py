from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import SmallInteger
from sqlalchemy import Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
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

    def __repr__(self):
        return f"<User uuid={self.uuid!r}, email={self.email!r}>"


class Project(Base):
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

    def __repr__(self):
        return f"<Project uuid={self.uuid!r} owner={self.owner!r}, title={self.title!r}>"


class DeployToken(Base):
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

    def __repr__(self):
        return f"<DeployToken uuid={self.uuid!r} create_by={self.create_by!r}>"
