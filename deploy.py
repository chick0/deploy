from os import mkdir
from os.path import join
from os.path import exists
from os.path import dirname
from os.path import abspath
from os import environ
from secrets import token_bytes

from uvicorn import run
from dotenv import load_dotenv


if __name__ == "__main__":
    BASE_DIR = abspath(dirname(__file__))
    TEMP_DIR = join(BASE_DIR, "temp")
    DEPLOY_DIR = join(BASE_DIR, "deploy")

    if not exists(TEMP_DIR):
        mkdir(TEMP_DIR)

    if not exists(DEPLOY_DIR):
        mkdir(DEPLOY_DIR)

    environ['TEMP_DIR'] = TEMP_DIR
    environ['DEPLOY_DIR'] = DEPLOY_DIR

    # import env
    load_dotenv()

    # set jwt secret
    try:
        with open(".JWT_SECRET", mode="rb") as key_reader:
            key: bytes = key_reader.read()
    except FileNotFoundError:
        key: bytes = token_bytes(24)
        with open(".JWT_SECRET", mode="wb") as key_writer:
            key_writer.write(key)

    environ['JWT_SECRET'] = key.hex()

    run(
        app="app:app",
        host="127.0.0.1",
        port=28888,
        log_level="info",
    )
