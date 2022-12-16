from os import stat
from typing import Optional
from logging import getLogger

from flask import Blueprint
from flask import request

from .. import db
from ..models import User
from ..models import Project
from ..models import Token
from ..models import Deploy
from ..user import login_required
from .project import RE
from ..utils import get_from
from ..utils import response
from ..tools import get_user_email
from deploy import routes
from deploy.path import upload_path_with_deploy_id

bp = Blueprint("api", __name__, url_prefix="/api")
bp.register_blueprint(routes.bp)

logger = getLogger()


def get_size(user_id: int, deploy_id: int) -> Optional[int]:
    try:
        return stat(upload_path_with_deploy_id(user_id, deploy_id)).st_size
    except FileNotFoundError:
        return None


@bp.get("/project/<int:project_id>")
@login_required
def project_detail(project_id: int, user: User):
    if user.id == 1:
        project: Project = Project.query.filter_by(
            id=project_id
        ).first()
    else:
        project: Project = Project.query.filter_by(
            id=project_id,
            owner=user.id
        ).first()

    if project is None:
        return response(
            status=False,
            message="등록된 프로젝트가 아닙니다."
        )

    deploy_list: list[Deploy] = Deploy.query.filter_by(
        project=project.id
    ).all()

    return response(
        payload={
            "last_deploy": project.last_deploy,
            "deploy_list": [
                {
                    "id": x.id,
                    "owner": get_user_email(x.owner),
                    "created_at": x.created_at.timestamp(),
                    "is_success": x.is_success,
                    "message": x.message,
                    "size": get_size(x.owner, x.id)
                }
                for x in deploy_list
            ]
        }
    )


@bp.delete("/token/<int:token_id>")
@login_required
def delete_token(token_id: int, user: User):
    token: Token = Token.query.filter_by(
        id=token_id,
    ).first()

    if token is None:
        return response(
            status=False,
            message="등록된 배포 토큰이 아닙니다."
        )

    if user.id == 1:
        pass
    elif user.id != token.owner:
        return response(
            status=False,
            message="본인의 배포 토큰만 삭제 할 수 있습니다."
        )

    db.session.delete(token)
    db.session.commit()

    logger.info(f"Deploy token id {token.id} is deleted by {user.email!r} from {get_from()}")

    return response(
        message="배포 토큰이 삭제되었습니다."
    )


@bp.post("/token/test")
def token_test():
    name: str = request.headers.get("x-deploy-name", "")

    if len(name) == 0:
        return response(
            status=False,
            message="프로젝트 이름이 없습니다."
        )

    match = RE.match(name)

    if match is None:
        return response(
            status=False,
            message="프로젝트 이름이 올바르지 않습니다."
        )

    token: str = request.headers.get("x-deploy-token", "")

    if len(token) == 0:
        return response(
            status=False,
            message="배포 토큰이 없습니다."
        )

    project: Project = Project.query.filter_by(
        name=name
    ).first()

    if project is None:
        return response(
            status=False,
            message="등록된 프로젝트가 아닙니다."
        )

    tk: Token = Token.query.filter_by(
        project=project.id,
        token=token
    ).first()

    if tk is None:
        return response(
            status=False,
            message="등록된 배포 토큰이 아닙니다."
        )

    return response(
        message="배포 토큰 테스트에 성공했습니다!"
    )
