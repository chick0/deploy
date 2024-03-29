from app import db

PREFIX = "dp_"

USER_ID = PREFIX + "user.id"
PROJECT_ID = PREFIX + "project.id"
DEPLOY_ID = PREFIX + "deploy.id"


class User(db.Model):  # type: ignore
    __tablename__ = PREFIX + "user"

    id = db.Column(
        db.Integer,
        unique=True,
        primary_key=True,
        nullable=False
    )

    email = db.Column(
        db.String(256),
        unique=True,
        nullable=False,
    )

    password = db.Column(
        db.String(128),
        nullable=False,
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
    )

    last_login_at = db.Column(
        db.DateTime,
        nullable=True,
    )

    password_updated_at = db.Column(
        db.DateTime,
        nullable=True,
    )


class Project(db.Model):  # type: ignore
    __tablename__ = PREFIX + "project"

    id = db.Column(
        db.Integer,
        unique=True,
        primary_key=True,
        nullable=False
    )

    owner = db.Column(
        db.Integer,
        db.ForeignKey(USER_ID),
        nullable=False
    )

    name = db.Column(
        db.String(100),
        unique=True,
        nullable=False,
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
    )

    last_deploy = db.Column(
        db.Integer,
        nullable=True,
    )


class Token(db.Model):  # type: ignore
    __tablename__ = PREFIX + "token"

    id = db.Column(
        db.Integer,
        unique=True,
        primary_key=True,
        nullable=False
    )

    owner = db.Column(
        db.Integer,
        db.ForeignKey(USER_ID),
        nullable=False
    )

    project = db.Column(
        db.Integer,
        db.ForeignKey(PROJECT_ID),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
    )

    expired_at = db.Column(
        db.DateTime,
        nullable=True,
    )

    last_used_at = db.Column(
        db.DateTime,
        nullable=True,
    )

    token = db.Column(
        db.String(100),
        nullable=False,
    )


class Deploy(db.Model):  # type: ignore
    __tablename__ = PREFIX + "deploy"

    id = db.Column(
        db.Integer,
        unique=True,
        primary_key=True,
        nullable=False
    )

    owner = db.Column(
        db.Integer,
        db.ForeignKey(USER_ID),
        nullable=False
    )

    project = db.Column(
        db.Integer,
        db.ForeignKey(PROJECT_ID),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
    )

    is_success = db.Column(
        db.Boolean,
        nullable=True
    )

    message = db.Column(
        db.Text,
        nullable=True,
    )
