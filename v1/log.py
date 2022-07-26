from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends

from sql import get_session
from sql.models import DeployLog
from v1.const import auth
from v1.models.log import LogID
from v1.models.log import LogIDList
from v1.models.log import Log
from utils.token.auth import parse_token
from utils.check import check_project
from utils.type import DeployLogType

router = APIRouter(
    tags=["Log"]
)


@router.get(
    "/log/{uuid}",
    description="프로젝트 배포 로그 목록을 가져옵니다.",
    response_model=LogIDList
)
# pylint: disable=missing-function-docstring
async def get_deploy_log_list(uuid: str, token=Depends(auth)):
    payload = parse_token(token=token)
    session = get_session()
    check_project(
        session=session,
        uuid=uuid,
        user=payload.user
    )

    try:
        return LogIDList(
            logIDList=[
                LogID(**x)
                for x in session.query(DeployLog).filter_by(
                    project=uuid
                ).filter(
                    DeployLog.type != DeployLogType.COMMAND.value
                ).with_entities(
                    DeployLog.id,
                    DeployLog.create_by,
                    DeployLog.type,
                    DeployLog.created_at,
                    DeployLog.return_code,
                ).order_by(
                    DeployLog.created_at.desc()
                ).all()
            ]
        )
    finally:
        session.close()


@router.get(
    "/log/{uuid}/{log_id}",
    description="해당 배포 로그의 자세한 정보를 가져옵니다.",
    response_model=Log
)
# pylint: disable=missing-function-docstring
async def get_detail_of_deploy_log(uuid: str, log_id: int, token=Depends(auth)):
    payload = parse_token(token=token)
    session = get_session()
    check_project(
        session=session,
        uuid=uuid,
        user=payload.user
    )

    dpl: DeployLog = session.query(DeployLog).filter_by(
        id=log_id,
        project=uuid
    ).first()

    if dpl is None:
        session.close()
        raise HTTPException(
            status_code=404,
            detail={
                "msg": "등록된 로그가 아닙니다."
            }
        )

    try:
        return Log(
            **dpl.__dict__,
            child=None if dpl.type == DeployLogType.UPLOAD.value
            else Log(**session.query(DeployLog).filter_by(
                called_by=dpl.id
            ).first().__dict__)
        )
    finally:
        session.close()
