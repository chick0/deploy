from jwt import encode
from jwt import decode
# from jwt.exceptions import ?
from fastapi import HTTPException
from pydantic import BaseModel

from . import key
from . import algorithms
from . import iss


class AuthPayload(BaseModel):
    user: str
    # registered claim #
    iss: str = iss


def create_token(user: str) -> str:
    return encode(
        payload=AuthPayload(
            user=user,
        ).dict(),
        key=key,
        algorithm=algorithms[0]
    )


def parse_token(token: str) -> AuthPayload:
    return decode(
        jwt=token,
        key=key,
        algorithms=algorithms
    )
