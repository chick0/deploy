from typing import Optional
from typing import NamedTuple

from flask import request
from flask import session
from flask import flash
from flask import redirect

from . import db
from .models import User
from .models import Project
from .models import Deploy
from .models import Token
from deploy.remove import remove_user_path_with_user_id
from deploy.remove import remove_upload_path_with_deploy_id
from deploy.remove import remove_unzip_path_with_deploy_id
from deploy.remove import remove_project_path_with_name


class Device(NamedTuple):
    device: str
    os: str
    browser: str


def get_ip() -> str:
    ip = request.remote_addr

    if ip is None:
        return request.headers.get("asdf", "?")

    return ip


def get_user_agent() -> str:
    return request.user_agent.string


def get_from() -> str:
    return f"({get_ip()!r}, {get_user_agent()!r})"


def logout(message: str, category: str = "message"):
    for key in list(session.keys()):
        del session[key]

    flash(message, category)
    return redirect("/")


def response(status: bool = True, message: Optional[str] = None, payload: dict = {}) -> tuple[dict, int]:
    return {
        "status": status,
        "message": message,
        "payload": payload
    }, 200 if status is True else 400


def get_page(name: str = "page", min: int = 0) -> int:
    page = request.args.get(name, "None")

    try:
        page = int(page) - 1

        if page < min:
            return min
    except ValueError:
        return min

    return page


def delete_user_from_system(user: User):
    for token in Token.query.filter(
        Token.owner == user.id
    ).all():
        db.session.delete(token)

    for deploy in Deploy.query.filter(
        Deploy.owner == user.id
    ).all():
        db.session.delete(deploy)

    remove_user_path_with_user_id(user.id)

    for project in Project.query.filter(
        Project.owner == user.id
    ).all():
        for token in Token.query.filter(
            Token.project == project.id
        ).all():
            db.session.delete(token)

        for deploy in Deploy.query.filter(
            Deploy.project == project.id
        ).all():
            remove_upload_path_with_deploy_id(deploy.owner, deploy.id)
            remove_unzip_path_with_deploy_id(deploy.id)
            db.session.delete(deploy)

        remove_project_path_with_name(project.name)
        db.session.delete(project)

    db.session.delete(user)
    db.session.commit()
