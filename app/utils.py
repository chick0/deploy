from typing import Optional
from typing import NamedTuple

from flask import request


class Device(NamedTuple):
    device: str
    os: str
    browser: str


def get_ip() -> str:
    ip = request.remote_addr

    if ip is None:
        return request.headers.get("asdf", "?")

    return ip


def get_user_agent() -> str:
    return request.user_agent.string


def get_from() -> str:
    return f"({get_ip()!r}, {get_user_agent()!r})"


def response(status: bool = True, message: Optional[str] = None, payload: dict = {}) -> tuple[dict, int]:
    return {
        "status": status,
        "message": message,
        "payload": payload
    }, 200 if status is True else 400
