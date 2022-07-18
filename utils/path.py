from os import urandom
from os import environ
from os.path import join


def get_project_path(owner: str, project: str) -> str:
    """
    Get project path

    :param owner: user(owner) uuid
    :param project: project uuid
    :return: path string
    """
    return join(
        environ['DEPLOY_DIR'],
        owner,
        project
    )


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
