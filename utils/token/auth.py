from jwt import encode
from jwt import decode
from fastapi.security.http import HTTPAuthorizationCredentials
from pydantic import BaseModel

from utils.token import key
from utils.token import algorithms
from utils.token import iss
from utils.token import iat
from utils.token import exp


class AuthPayload(BaseModel):
    user: str
    # registered claim #
    iss: str = iss
    iat: int
    exp: int


def create_token(user: str) -> str:
    return encode(
        payload=AuthPayload(
            user=user,
            iat=iat(),
            exp=exp()
        ).dict(),
        key="auth:" + key,
        algorithm=algorithms[0]
    )


def parse_token(token: str or HTTPAuthorizationCredentials) -> AuthPayload:
    if isinstance(token, HTTPAuthorizationCredentials):
        token = token.credentials

    return decode(
        jwt=token,
        key="auth:" + key,
        algorithms=algorithms
    )
