from logging import getLogger

from flask import Blueprint

from .. import db
from ..models import User
from ..models import Project
from ..models import Token
from ..user import login_required
from ..utils import get_from
from ..utils import response
from deploy import routes
from deploy.utils import auth_required

bp = Blueprint("api", __name__, url_prefix="/api")
bp.register_blueprint(routes.bp)

logger = getLogger()


@bp.delete("/token/<int:token_id>")
@login_required
def delete_token(token_id: int, user: User):
    token = Token.query.filter(
        Token.id == token_id
    ).first()

    if token is None:
        return response(
            status=False,
            message="등록된 배포 토큰이 아닙니다."
        )

    if user.id != 1 and user.id != token.owner:
        return response(
            status=False,
            message="본인의 배포 토큰만 삭제 할 수 있습니다."
        )

    db.session.delete(token)
    db.session.commit()

    logger.info(f"Deploy token id {token.id} is deleted by {user.email} from {get_from()}")

    return response(
        message="배포 토큰이 삭제되었습니다."
    )


@bp.post("/token/test")
@auth_required
def token_test(project: Project, token: Token):
    return response(
        message="배포 토큰 테스트에 성공했습니다!"
    )
