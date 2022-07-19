from hashlib import sha512
from datetime import datetime

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sql import get_session
from sql.models import User
from v1.const import auth
from v1.models.auth import TokenVerify
from v1.models.auth import LoginRequest
from v1.models.auth import LoginResponse
from utils.token.auth import create_token
from utils.token.auth import parse_token

router = APIRouter(
    tags=["Auth"]
)


@router.get(
    "/auth",
    description="인증 토큰을 검사합니다.",
    response_model=TokenVerify
)
# pylint: disable=missing-function-docstring
async def verify_auth_token(token=Depends(auth)):
    try:
        parse_token(token=token)
    # pylint: disable=broad-except
    except (HTTPException, Exception):
        return TokenVerify(
            result=False
        )

    return TokenVerify(
        result=True
    )


@router.post(
    "/auth",
    description="아이디와 비밀번호로 로그인 합니다.",
    response_model=LoginResponse
)
# pylint: disable=missing-function-docstring
async def create_auth_token(request: LoginRequest):
    session = get_session()
    user: User = session.query(User).filter_by(
        email=request.email,
        password=sha512(request.password.encode()).hexdigest()
    ).first()

    if user is None:
        raise HTTPException(
            status_code=400,
            detail={
                "msg": "등록된 사용자가 아닙니다."
            }
        )

    uuid = user.uuid

    user.last_login_at = datetime.now()

    try:
        return LoginResponse(
            token=create_token(
                user=uuid
            )
        )
    finally:
        session.commit()
        session.close()
