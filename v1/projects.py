from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends

from sql import get_session
from sql.models import User
from sql.models import Project
from v1.const import auth
from v1.models.projects import Project as ProjectModel
from v1.models.projects import ProjectList
from utils.token.auth import parse_token

router = APIRouter(
    tags=["Projects"]
)


@router.get(
    "/projects",
    description="등록한 프로젝트 목록을 확인합니다.",
    response_model=ProjectList
)
# pylint: disable=missing-function-docstring
async def get_projects_list(token=Depends(auth)):
    payload = parse_token(token=token)
    session = get_session()

    if session.query(User).filter_by(
        uuid=payload.user
    ).first() is None:
        raise HTTPException(
            status_code=404,
            detail={
                "msg": "등록된 유저가 아닙니다."
            }
        )

    try:
        return ProjectList(
            projectList=[
                ProjectModel(
                    uuid=ctx.uuid,
                    title=ctx.title,
                    owner=ctx.owner,
                    type=ctx.type,
                    path=ctx.path
                )
                for ctx in session.query(Project).filter_by(
                    owner=payload.user
                ).order_by(
                    Project.created_at.desc()
                ).all()
            ]
        )
    finally:
        session.close()
