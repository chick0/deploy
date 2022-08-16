from os import name as os_name
from datetime import datetime

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from sql import get_session
from sql.models import Project
from v1.const import auth
from v1.const import any_
from v1.models.project import ProjectCreate
from v1.models.project import ProjectCreated
from v1.models.project import Project as ProjectModel
from v1.models.project import ProjectUpdateResult
from utils.token.auth import parse_token as parse_auth_token
from utils.token.deploy import parse_token as parse_deploy_token
from utils.check import check_project
from utils.type import ProjectType
from utils.type import verify_type
from utils.uuid import get_uuid

router = APIRouter(
    tags=["Project"]
)


@router.post(
    "/project",
    description="새로운 프로젝트를 등록합니다.",
    response_model=ProjectCreated
)
# pylint: disable=missing-function-docstring
async def create_project(request: ProjectCreate, token=Depends(auth)):
    payload = parse_auth_token(token=token)

    if not verify_type(project_type=request.type):
        raise HTTPException(
            status_code=400,
            detail={
                "msg": "프로젝트 유형이 올바르지 않습니다."
            }
        )

    uuid = get_uuid()
    title = request.title.strip()

    project = Project()
    project.uuid = uuid
    project.title = title
    project.owner = payload.user
    project.created_at = datetime.now()
    project.type = request.type

    if project.type != ProjectType.FRONTEND.value:
        if os_name == "nt":
            raise HTTPException(
                status_code=500,
                detail={
                    "msg": "해당 기능은 윈도우 서버에서 사용할 수 없습니다."
                }
            )

        project.path = request.path.strip()
        project.command = request.command.strip()

        if len(project.path) == 0:
            raise HTTPException(
                status_code=400,
                detail={
                    "msg": "프로젝트 경로는 빈칸이 될 수 없습니다."
                }
            )
    else:
        project.path = ""
        project.command = ""

    if len(project.title) == 0:
        raise HTTPException(
            status_code=400,
            detail={
                "msg": "프로젝트 제목은 빈칸이 될 수 없습니다."
            }
        )

    session = get_session()
    session.add(project)

    try:
        session.commit()
    except IntegrityError as _error:
        raise HTTPException(
            status_code=400,
            detail={
                "msg": "프로젝트를 생성하는 과정에서 오류가 발생했습니다."
            }
        ) from _error
    # pylint: disable=broad-except
    except Exception as _error:
        raise HTTPException(
            status_code=500,
            detail={
                "msg": "프로젝트를 생성하는 과정에서 알 수 없는 오류가 발생했습니다."
            }
        ) from _error
    finally:
        session.close()

    return ProjectCreated(
        uuid=uuid,
        title=title
    )


@router.get(
    "/project/{uuid}",
    description="등록된 프로젝트 정보를 불러옵니다.",
    response_model=ProjectModel
)
# pylint: disable=missing-function-docstring
async def get_project_data(uuid: str, token=Depends(any_)):
    try:
        payload = parse_auth_token(token=token)
        token = "auth"
    # pylint: disable=broad-except
    except (HTTPException, Exception) as _error:
        payload = parse_deploy_token(token=token)
        token = "deploy"

        if not payload.permission.read:
            raise HTTPException(
                status_code=403,
                detail={
                    "msg": "해당 배포 토큰은 프로젝트를 조회할 권한이 없습니다."
                }
            ) from _error

    session = get_session()

    if token == "auth":
        project: Project = check_project(
            session=session,
            uuid=uuid,
            user=payload.user
        )
    else:
        # token type can be "auth" or "deploy"
        # in this case token must be "deploy token"
        # but pylint scan this to "auth token"
        # so this warning has been ignored
        project: Project = check_project(
            session=session,
            # pylint: disable=no-member
            uuid=payload.project,
            user=payload.user
        )

    try:
        return ProjectModel(**project.__dict__)
    finally:
        session.close()


@router.patch(
    "/project",
    description="등록된 프로젝트 정보를 수정합니다.",
    response_model=ProjectUpdateResult
)
# pylint: disable=missing-function-docstring
async def edit_project_data(request: ProjectModel, token=Depends(any_)):
    try:
        payload = parse_auth_token(token=token)
    except HTTPException:
        payload = parse_deploy_token(token=token)
        if request.uuid != payload.project:
            return ProjectUpdateResult(
                result=False,
                reason="해당 배포 토큰은 해당 프로젝트을 관리 할 수 없습니다."
            )

        if not payload.permission.write:
            return ProjectUpdateResult(
                result=False,
                reason="해당 배포 토큰은 프로젝트를 수정할 권한이 없습니다."
            )

    if not verify_type(project_type=request.type):
        return ProjectUpdateResult(
            result=False,
            reason="프로젝트 유형이 올바르지 않습니다."
        )

    session = get_session()
    project: Project = session.query(Project).filter_by(
        uuid=request.uuid,
        owner=payload.user
    )

    project.title = request.title.strip()
    project.type = request.type
    project.path = request.path.strip()

    if len(project.title) == 0:
        session.close()
        return ProjectUpdateResult(
            result=False,
            reason="프로젝트 제목은 빈칸이 될 수 없습니다."
        )

    session.commit()

    try:
        return ProjectUpdateResult(
            result=True,
            reason="등록된 프로젝트가 수정되었습니다."
        )
    finally:
        session.close()


@router.delete(
    "/project/{uuid}",
    description="등록된 프로젝트를 삭제합니다.",
    response_model=ProjectUpdateResult
)
# pylint: disable=missing-function-docstring
async def delete_project(uuid: str, token=Depends(auth)):
    payload = parse_auth_token(token=token)

    session = get_session()
    project: Project = session.query(Project).filter_by(
        uuid=uuid,
        owner=payload.user
    ).first()

    if project is None:
        return ProjectUpdateResult(
            result=False,
            reason="등록된 프로젝트가 아닙니다."
        )

    title = project.title

    session.delete(project)
    session.commit()

    try:
        return ProjectUpdateResult(
            result=True,
            reason=f"'{title}' 프로젝트가 삭제되었습니다."
        )
    finally:
        session.close()
