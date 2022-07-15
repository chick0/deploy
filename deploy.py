from os import environ
from secrets import token_bytes

from uvicorn import run
from dotenv import load_dotenv


if __name__ == "__main__":
    # import env
    load_dotenv()

    # set jwt secret
    try:
        key: bytes = open(".JWT_SECRET", mode="rb").read()
    except (FileNotFoundError, Exception):
        key: bytes = token_bytes(24)
        open(".JWT_SECRET", mode="wb").write(key)

    environ.__setitem__("JWT_SECRET", key.hex())

    run(
        app="app:app",
        host="127.0.0.1",
        port=28888,
        log_level="info",
    )
