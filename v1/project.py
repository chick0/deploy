from fastapi import APIRouter

from v1.models.project import ProjectCreate
from v1.models.project import Project
from v1.models.project import ProjectUpdateResult

router = APIRouter(
    tags=["Project"]
)


@router.post(
    "/project",
    description="새로운 프로젝트를 등록합니다.",
    response_model=Project
)
async def create_project(request: ProjectCreate):
    return {}


@router.get(
    "/project/:uuid",
    description="등록된 프로젝트 정보를 불러옵니다.",
    response_model=Project
)
async def get_project_data(uuid: str):
    return {}


@router.patch(
    "/project",
    description="등록된 프로젝트 정보를 수정합니다.",
    response_model=ProjectUpdateResult
)
async def edit_project_data(request: Project):
    return {}


@router.delete(
    "/project/:uuid",
    description="등록된 프로젝트를 삭제합니다.",
    response_model=ProjectUpdateResult
)
async def delete_project(uuid: str):
    return {}
