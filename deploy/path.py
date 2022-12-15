from os.path import join
from typing import Optional

from app.models import Project
from . import UPLOAD_DIR
from . import PROJECT_DIR
from . import UNZIP_DIR
from . import create_dir


def upload_path_with_deploy_id(user_id: int, deploy_id: int) -> str:
    folder = join(UPLOAD_DIR, str(user_id))
    create_dir(folder)

    return join(folder, str(deploy_id) + ".zip")


def unzip_path_with_deploy_id(deploy_id: int) -> str:
    return join(UNZIP_DIR, str(deploy_id))


def project_path_with_id(project_id: int) -> Optional[str]:
    project: Project = Project.query.with_entities(
        Project.name
    ).filter_by(
        id=project_id
    ).first()

    if project is None:
        return None

    return project_path_with_name(project.name)


def project_path_with_name(name: str) -> str:
    folder = join(PROJECT_DIR, name)
    create_dir(folder)

    return folder
