from os import remove
from shutil import rmtree

from .path import upload_path_with_deploy_id
from .path import unzip_path_with_deploy_id
from .path import project_path_with_name
from .path import user_path_with_user_id


def _safe_rmtree(path: str) -> None:
    try:
        rmtree(path)
    except FileNotFoundError:
        pass


def remove_user_path_with_user_id(user_id: int) -> None:
    # dir
    _safe_rmtree(user_path_with_user_id(user_id))


def remove_upload_path_with_deploy_id(user_id: int, deploy_id: int) -> None:
    # file
    try:
        remove(upload_path_with_deploy_id(user_id, deploy_id))
    except FileNotFoundError:
        pass


def remove_unzip_path_with_deploy_id(deploy_id: int) -> None:
    # dir
    _safe_rmtree(unzip_path_with_deploy_id(deploy_id))


def remove_project_path_with_name(name: str) -> None:
    # dir
    _safe_rmtree(project_path_with_name(name))
