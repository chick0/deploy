from jwt import encode
from jwt import decode
from jwt.exceptions import DecodeError
from fastapi import HTTPException
from fastapi.security.http import HTTPAuthorizationCredentials
from pydantic import BaseModel

from utils.token import key
from utils.token import algorithms
from utils.token import iss
from utils.token import iat
from utils.token import exp


class AuthPayload(BaseModel):
    """
    Payload for Auth token
    """
    user: str
    # registered claim #
    iss: str = iss
    iat: int
    exp: int


def create_token(user: str) -> str:
    """
    Create Auth token

    :param user: user uuid
    :return: jwt token
    """
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
    """
    Parse Auth token

    :param token: auth token
    :return: Auth token payload
    """
    if isinstance(token, HTTPAuthorizationCredentials):
        token = token.credentials

    try:
        return AuthPayload(**decode(
            jwt=token,
            key="auth:" + key,
            algorithms=algorithms,
            issuer=iss
        ))
    except DecodeError as decode_fail:
        raise HTTPException(
            status_code=400,
            detail={
                "msg": "배포 토큰이 올바르지 않습니다."
            }
        ) from decode_fail
