from jwt import encode
from jwt import decode
# from jwt.exceptions import ?
from fastapi import HTTPException
from pydantic import BaseModel

from utils.token import key
from utils.token import algorithms
from utils.token import iss


class DeployPermission(BaseModel):
    read: bool
    write: bool
    delete: bool


class DeployPayload(BaseModel):
    user: str
    project: str
    permission: DeployPermission
    # registered claim #
    iss: str = iss


def create_token(user: str, project: str, permission: list) -> str:
    options = {}
    [options.update({x: False}) for x in DeployPermission.schema()['properties']]

    for x in [x.lower() for x in permission]:
        if x in DeployPermission.schema()['properties']:
            options[x] = True
        else:
            raise TypeError(f"'{x}' it not allowed permission.")

    return encode(
        payload=DeployPayload(
            user=user,
            project=project,
            permission=DeployPermission(**options)
        ).dict(),
        key=key,
        algorithm=algorithms[0]
    )


def parse_token(token: str) -> DeployPayload:
    return decode(
        jwt=token,
        key=key,
        algorithms=algorithms
    )
