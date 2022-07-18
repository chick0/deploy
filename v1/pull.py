from fastapi import APIRouter
from fastapi import Depends

from sql import get_session
from sql.models import Project
from v1.const import deploy
from v1.models.pull import PullResult
from utils.token.deploy import parse_token
from utils.type import ProjectType

router = APIRouter(
    tags=["Pull"]
)


@router.post(
    "/pull",
    description="소스코드의 변경 사항을 적용합니다.",
    response_model=PullResult
)
# pylint: disable=missing-function-docstring
async def pull_and_deploy(token=Depends(deploy)):
    payload = parse_token(token=token)
    if not payload.permission.write:
        return PullResult(
            result=False,
            reason="쓰기 권한이 없어 해당 토큰을 사용 할 수 없습니다."
        )

    session = get_session()
    project: Project = session.query(Project).filter_by(
        uuid=payload.project
    ).first()

    if project is None:
        session.close()
        return PullResult(
            result=False,
            reason="등록된 프로젝트가 아닙니다."
        )

    if project.type == ProjectType.FRONTEND.value:
        session.close()
        return PullResult(
            result=False,
            reason="프론트 프로젝트는 해당 방식으로 배포 할 수 없습니다."
        )

    # TODO:git pull
    # TODO:restart with command

    return {}
