from secrets import token_bytes

PATH = ".key"
KEY_SIZE = 48


class KeySizeError(Exception):
    def __init__(self) -> None:
        super().__init__()


def get_key() -> bytes:
    try:
        with open(PATH, mode="rb") as reader:
            key = reader.read()

            if len(key) < KEY_SIZE:
                print("KEY_SIZE_ERROR")
                raise KeySizeError

            return key
    except (FileNotFoundError, KeySizeError):
        key = token_bytes(KEY_SIZE)

        with open(PATH, mode="wb") as writer:
            writer.write(key)

        return key
