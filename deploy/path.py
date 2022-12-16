from os.path import join

from . import UPLOAD_DIR
from . import PROJECT_DIR
from . import UNZIP_DIR
from . import create_dir


def user_path_with_user_id(user_id: int) -> str:
    folder = join(UPLOAD_DIR, str(user_id))
    create_dir(folder)

    return folder


def upload_path_with_deploy_id(user_id: int, deploy_id: int) -> str:
    folder = user_path_with_user_id(user_id)
    return join(folder, str(deploy_id) + ".zip")


def unzip_path_with_deploy_id(deploy_id: int) -> str:
    return join(UNZIP_DIR, str(deploy_id))


def project_path_with_name(name: str) -> str:
    folder = join(PROJECT_DIR, name)
    create_dir(folder)

    return folder
