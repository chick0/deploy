from os import mkdir
from shutil import rmtree
from zipfile import ZipFile
from datetime import datetime

from fastapi import APIRouter
from fastapi import Depends
from fastapi import UploadFile
from aiofiles import open as aio_open

from sql import Session
from sql import get_session
from sql.models import Project
from sql.models import DeployLog
from v1.const import deploy
from v1.models.upload import UploadResult
from utils.token.deploy import parse_token
from utils.path import get_project_path
from utils.path import get_temp_path
from utils.type import ProjectType
from utils.type import DeployLogType

router = APIRouter(
    tags=["Upload"]
)


def create_log(session: Session, project: str, user: str, return_code: int):
    """
    Create frontend deploy log

    :param session: database connect session
    :param project: project uuid
    :param user: user uuid
    :param return_code: aka error code
    :return: *none*
    """
    upload_log = DeployLog()
    upload_log.project = project
    upload_log.create_by = user
    upload_log.type = DeployLogType.UPLOAD.value
    upload_log.created_at = datetime.now()
    upload_log.return_code = return_code

    session.add(upload_log)
    session.commit()


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

    head = await file.read(size=3)

    if not head.startswith(b"PK"):
        create_log(
            session=session,
            project=project.uuid,
            user=payload.user,
            return_code=-1
        )

        session.close()
        return UploadResult(
            result=False,
            reason="압축 파일을 업로드 해야 합니다.."
        )

    project_path = get_project_path(
        owner=project.owner,
        project=project.created_at
    )

    try:
        rmtree(path=project_path)
    except (FileNotFoundError, PermissionError):
        create_log(
            session=session,
            project=project.uuid,
            user=payload.user,
            return_code=-2
        )

        session.close()
        return UploadResult(
            result=False,
            reason="기존 파일 삭제에 실패했습니다."
        )

    mkdir(path=project_path)

    await file.seek(0)

    zipfile_path = get_temp_path(
        owner=project.owner,
        project=project.uuid
    )

    async with aio_open(zipfile_path, 'wb') as writer:
        # async chunk read/write
        while content := await file.read(1024):
            await writer.write(content)

    with ZipFile(file=zipfile_path) as zip_ctx:
        zip_ctx.extractall(
            path=project_path
        )

    create_log(
        session=session,
        project=project.uuid,
        user=payload.user,
        return_code=0
    )

    try:
        return UploadResult(
            result=True
        )
    finally:
        session.close()
