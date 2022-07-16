from fastapi import APIRouter

from v1.models.auth import LoginRequest
from v1.models.auth import LoginResponse
from utils.token.auth import create_token

router = APIRouter(
    tags=["Auth"]
)


@router.post(
    "/auth",
    description="아이디와 비밀번호로 로그인 합니다.",
    response_model=LoginResponse
)
async def create_token_for_login(request: LoginRequest):
    return {}
