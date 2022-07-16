from fastapi import APIRouter

from v1.models.token import TokenRequest
from v1.models.token import TokenResponse
from v1.models.token import TokenDelete
from v1.models.token import TokenDeleteResult
from utils.token.deploy import create_token

router = APIRouter(
    tags=["Token"]
)


@router.post(
    "/token",
    description="프로젝트 배포에 사용할 토큰을 생성합니다.",
    response_model=TokenResponse
)
async def create_token_for_deploy(request: TokenRequest):
    return {}


@router.delete(
    "/token",
    description="등록된 토큰을 삭제합니다.",
    response_model=TokenDeleteResult
)
async def delete_deploy_token(request: TokenDelete):
    return {}
