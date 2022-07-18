from fastapi import APIRouter
from fastapi import Depends

from v1.const import deploy
from v1.models.pull import PullResult

router = APIRouter(
    tags=["Pull"]
)


@router.post(
    "/pull/:uuid",
    description="소스코드의 변경 사항을 적용합니다.",
    response_model=PullResult
)
async def pull_and_deploy(uuid: str, token=Depends(deploy)):
    return {}
