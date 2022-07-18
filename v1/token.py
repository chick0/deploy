from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sql import get_session
from sql.models import User
from sql.models import Project
from sql.models import DeployToken
from v1.const import auth
from v1.models.token import TokenRequest
from v1.models.token import TokenResponse
from v1.models.token import TokenDelete
from v1.models.token import TokenDeleteResult
from utils.token.auth import parse_token
from utils.token.deploy import parse_permission
from utils.token.deploy import create_token
from utils.token.deploy import parse_token as parse_deploy_token
from utils.uuid import get_uuid

router = APIRouter(
    tags=["Token"]
)


@router.post(
    "/token",
    description="프로젝트 배포에 사용할 토큰을 생성합니다.",
    response_model=TokenResponse
)
async def create_token_for_deploy(request: TokenRequest, token=Depends(auth)):
    payload = parse_token(token=token)
    session = get_session()

    user: User = session.query(User).filter_by(
        uuid=payload.user
    ).first()

    if user is None:
        raise HTTPException(
            status_code=403,
            detail={
                "msg": "등록된 사용자가 아닙니다."
            }
        )

    project: Project = session.query(Project).filter_by(
        uuid=request.project,
        owner=user.user
    ).first()

    if project is None:
        raise HTTPException(
            status_code=404,
            detail={
                "msg": "등록된 프로젝트가 아닙니다."
            }
        )

    permission = parse_permission(
        permission=request.permission
    )

    dpt = DeployToken()
    dpt.uuid = get_uuid()
    dpt.project = project.uuid
    dpt.create_by = user.uuid
    dpt.read = permission.read
    dpt.write = permission.write
    dpt.delete = permission.delete

    session.add(dpt)
    session.commit()

    try:
        return TokenResponse(
            token=create_token(
                uuid=dpt.uuid,
                user=payload.user,
                project=request.project,
                permission=request.permission
            )
        )
    finally:
        session.close()


@router.delete(
    "/token",
    description="등록된 토큰을 삭제합니다.",
    response_model=TokenDeleteResult
)
async def delete_deploy_token(request: TokenDelete, token=Depends(auth)):
    payload = parse_token(token=token)
    deploy = parse_deploy_token(token=request.token)

    if payload.user != deploy.user:
        return TokenDeleteResult(
            result=False,
            reason="배포 토큰을 생성한 사용자 만 배포 토큰을 삭제 할 수 있습니다."
        )

    session = get_session()

    dpt: DeployToken = session.query(DeployToken).filter_by(
        uuid=deploy.uuid,
        project=deploy.project,
        create_by=payload.user
    ).first()

    if dpt is None:
        return TokenDeleteResult(
            result=False,
            reason="해당 배포 토큰을 조회 할 수 없습니다. 이미 삭제되었거나 권한이 잘못되었습니다."
        )

    session.delete(dpt)
    session.commit()

    try:
        return TokenDeleteResult(
            result=True,
            reason="해당 배포 토큰을 삭제했습니다."
        )
    finally:
        session.close()
