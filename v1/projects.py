from fastapi import APIRouter
from fastapi import Depends

from v1.const import auth
from v1.models.projects import Project
from v1.models.projects import ProjectList

router = APIRouter(
    tags=["Projects"]
)


@router.get(
    "/projects",
    description="등록한 프로젝트 목록을 확인합니다.",
    response_model=ProjectList
)
async def get_projects_list(token=Depends(auth)):
    """
    Get project list with auth token

    :param token: auth token
    :return: projects list which I created
    """
    return {}
