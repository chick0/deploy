from os import environ
from os.path import join


def get_project_path(owner: str, project: str) -> str:
    return join(
        environ['DEPLOY_DIR'],
        owner,
        project
    )
