from jwt import encode
from jwt import decode
from fastapi import HTTPException
from fastapi.security.http import HTTPAuthorizationCredentials
from pydantic import BaseModel

from sql import get_session
from sql.models import DeployToken
from utils.token import key
from utils.token import algorithms
from utils.token import iss


class DeployPermission(BaseModel):
    """
    Permission model for deploy token
    """
    read: bool
    write: bool
    delete: bool


class DeployPayload(BaseModel):
    """
    Payload for deploy token
    """
    uuid: str
    user: str
    project: str
    permission: DeployPermission
    # registered claim #
    iss: str = iss


def parse_permission(permission: list) -> DeployPermission:
    """
    Parse permission list to model

    :param permission: list of required permission
    :return: permission model
    """
    options = {}

    for prop in DeployPermission.schema()['properties']:
        if prop in permission:
            options[prop] = True
        else:
            options[prop] = False

    return DeployPermission(**options)


def create_token(uuid: str, user: str, project: str, permission: list) -> str:
    """
    Create Deploy token

    :param uuid: deploy token uuid
    :param user: user uuid
    :param project: project uuid
    :param permission: permission list
    :return: jwt token
    """
    return encode(
        payload=DeployPayload(
            uuid=uuid,
            user=user,
            project=project,
            permission=parse_permission(
                permission=permission
            )
        ).dict(),
        key="deploy:" + key,
        algorithm=algorithms[0]
    )


def parse_token(token: str or HTTPAuthorizationCredentials) -> DeployPayload:
    """
    Parse deploy token

    :param token: deploy token
    :return: Deploy token payload
    """
    if isinstance(token, HTTPAuthorizationCredentials):
        token = token.credentials

    payload = DeployPayload(**decode(
        jwt=token,
        key="deploy:" + key,
        algorithms=algorithms,
        issuer=iss
    ))

    session = get_session()

    if session.query(DeployToken).filter_by(
        uuid=payload.uuid
    ).count():
        raise HTTPException(
            status_code=400,
            detail={
                "msg": "삭제된 배포 토큰입니다."
            }
        )

    return payload
