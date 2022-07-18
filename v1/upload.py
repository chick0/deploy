from fastapi import APIRouter
from fastapi import Depends
from fastapi import UploadFile

from sql import get_session
from sql.models import Project
from v1.const import deploy
from v1.models.upload import UploadResult
from utils.token.deploy import parse_token
from utils.type import ProjectType

router = APIRouter(
    tags=["Upload"]
)


@router.post(
    "/upload",
    description="배포할 파일을 압축 파일로 업로드 합니다.",
    response_model=UploadResult
)
# pylint: disable=missing-function-docstring
async def upload_and_deploy(file: UploadFile, token=Depends(deploy)):
    payload = parse_token(token=token)
    if not payload.permission.write:
        return UploadResult(
            result=False,
            reason="쓰기 권한이 없어 해당 토큰을 사용 할 수 없습니다."
        )

    session = get_session()

    project: Project = session.query(Project).filter_by(
        uuid=payload.project
    ).first()

    if project is None:
        session.close()
        return UploadResult(
            result=False,
            reason="등록된 프로젝트가 아닙니다."
        )

    if project.type != ProjectType.FRONTEND.value:
        session.close()
        return UploadResult(
            result=False,
            reason="프론트 프로젝트만 해당 방식으로 배포 할 수 있습니다."
        )

    stream = await file.read()

    head = stream[:3]
    if not head.startswith(b"PK"):
        session.close()
        return UploadResult(
            result=False,
            reason="압축 파일을 업로드 해야 합니다.."
        )

    # TODO:remove old file
    # TODO:unzip and move to project path

    return {}
