from os import mkdir
from os.path import join
from os.path import isdir
from os.path import dirname

BASE_DIR = dirname(dirname(__file__))

UPLOAD_DIR = join(BASE_DIR, "upload")
PROJECT_DIR = join(BASE_DIR, "project")
UNZIP_DIR = join(BASE_DIR, "unzip")


def create_dir(path: str):
    if not isdir(path):
        mkdir(path)


if __name__ != "__main__":
    create_dir(UPLOAD_DIR)
    create_dir(PROJECT_DIR)
    create_dir(UNZIP_DIR)
