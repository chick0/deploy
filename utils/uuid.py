from uuid import uuid4


def get_uuid() -> str:
    """
    Get UUIDv4 string

    :return: uuid string
    """
    return str(uuid4())
