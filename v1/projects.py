from fastapi import APIRouter

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
async def get_projects_list():
    return {}
