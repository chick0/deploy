from flask import g

from .models import Project


def get_g_cache(key: str):
    try:
        return getattr(g, key)
    except AttributeError:
        return None


def set_g_cache(key: str, value) -> None:
    setattr(g, key, value)


def get_project_name(project_id: int) -> str:
    key = f"project-name:{project_id}"
    name = get_g_cache(key)

    if name is None:
        project: Project = Project.query.with_entities(
            Project.name,
        ).filter_by(
            id=project_id
        ).first()

        if project is None:
            return "-"

        name = project.name
        set_g_cache(key, name)

    return name
