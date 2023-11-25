from flask import g

from .models import User
from .models import Project
from .models import Deploy


def get_g_cache(key: str):
    try:
        return getattr(g, key)
    except AttributeError:
        return None


def set_g_cache(key: str, value) -> None:
    setattr(g, key, value)


def get_project_name(project_id: int) -> str:
    key = f"project.{project_id}.name"
    name = get_g_cache(key)

    if name is None:
        project = Project.query.with_entities(
            Project.name,
        ).filter(
            Project.id == project_id
        ).first()

        if project is None:
            return "-"

        name = project.name
        set_g_cache(key, name)

    return name


def get_user_email(user_id: int) -> str:
    key = f"user.{user_id}.email"
    email = get_g_cache(key)

    if email is None:
        user = User.query.with_entities(
            User.email
        ).filter(
            User.id == user_id
        ).first()

        if user is None:
            raise ValueError("등록된 유저가 아닙니다.")

        email = user.email
        set_g_cache(key, email)

    return email


def get_deploy_created_at(deploy_id: int):
    key = f"deploy.{deploy_id}.created_at"
    created_at = get_g_cache(key)

    if created_at is None:
        deploy = Deploy.query.with_entities(
            Deploy.created_at
        ).filter(
            Deploy.id == deploy_id
        ).first()

        if deploy is None:
            raise ValueError("등록된 배포 정보가 아닙니다.")

        created_at = deploy.created_at
        set_g_cache(key, created_at)

    return created_at


def size2str(size: int) -> str:
    def round2str(a, b) -> str:
        return str(round(a, b))

    STEP = 1024
    KB = STEP
    MB = KB * STEP
    GB = MB * STEP

    if size >= GB:
        return round2str(size / GB, 2) + " GB"
    elif size >= MB:
        return round2str(size / MB, 2) + " MB"
    elif size >= KB:
        return round2str(size / KB, 2) + " KB"
    else:
        return str(size)
