from jwt import encode
from jwt import decode
from fastapi.security.http import HTTPAuthorizationCredentials
from pydantic import BaseModel

from utils.token import key
from utils.token import algorithms
from utils.token import iss


class DeployPermission(BaseModel):
    read: bool
    write: bool
    delete: bool


class DeployPayload(BaseModel):
    uuid: str
    user: str
    project: str
    permission: DeployPermission
    # registered claim #
    iss: str = iss


def parse_permission(permission: list) -> DeployPermission:
    options = {}
    [options.update({x: False}) for x in DeployPermission.schema()['properties']]

    for x in [x.lower() for x in permission]:
        if x in DeployPermission.schema()['properties']:
            options[x] = True
        else:
            raise TypeError(f"'{x}' it not allowed permission.")

    return DeployPermission(**options)


def create_token(uuid: str, user: str, project: str, permission: list) -> str:
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
    if isinstance(token, HTTPAuthorizationCredentials):
        token = token.credentials

    return decode(
        jwt=token,
        key="deploy:" + key,
        algorithms=algorithms
    )
