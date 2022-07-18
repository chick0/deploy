from os import urandom
from os import environ
from os import mkdir
from os.path import join
from os.path import exists


def get_project_path(owner: str, project: str) -> str:
    """
    Get project path

    :param owner: user(owner) uuid
    :param project: project uuid
    :return: path string
    """
    user_dir = join(
        environ['DEPLOY_DIR'],
        owner
    )

    if not exists(path=user_dir):
        mkdir(path=user_dir)

    project_dir = join(
        user_dir,
        project
    )

    if not exists(path=project_dir):
        mkdir(path=project_dir)

    return project_dir


def get_temp_path(owner: str, project: str) -> str:
    """
    Get path for save temp file
    * front deploy file

    :param owner: user(owner) uuid
    :param project: project uuid
    :return: "unique" path string
    """
    return join(
        environ['TEMP_DIR'],
        f"{owner}-{project}.{urandom(4).hex()}.zip"
    )
