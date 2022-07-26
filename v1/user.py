from fastapi import APIRouter
from fastapi import Depends

from sql import get_session
from sql.models import User
from utils.token.auth import parse_token
from v1.models.user import UserResponse
from v1.const import auth

router = APIRouter(
    tags=["User"],
)


@router.get(
    "/user/{uuid}",
    description="",
    response_model=UserResponse
)
# pylint: disable=missing-function-docstring
async def get_user_information(uuid: str, token=Depends(auth)):
    parse_token(token=token)
    session = get_session()

    user: User = session.query(User).filter_by(
        uuid=uuid
    ).with_entities(
        User.email
    ).first()

    if user is None:
        session.close()
        return UserResponse(
            name="ㅇㅇ"
        )

    try:
        return UserResponse(
            name=user.email.rsplit("@", 1)[0]
        )
    finally:
        session.close()
