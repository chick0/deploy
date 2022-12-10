from typing import Optional
from datetime import datetime

from flask import Blueprint
from flask import request

from .. import db
from ..models import User
from ..models import Project
from ..models import Token
from ..models import Deploy
from ..user import login_required
from .project import RE

bp = Blueprint("api", __name__, url_prefix="/api")


def resp(status: bool = True, message: Optional[str] = None, payload: dict = {}) -> tuple[dict, int]:
    return {
        "status": status,
        "message": message,
        "payload": payload
    }, 200 if status is True else 400


@bp.get("/project/<int:project_id>")
@login_required
def project_detail(project_id: int, user: User):
    if user.id == 1:
        project = Project.query.filter_by(
            id=project_id
        ).first()
    else:
        project = Project.query.filter_by(
            id=project_id,
            owner=user.id
        ).first()

    if project is None:
        return resp(
            status=False,
            message="등록된 프로젝트가 아닙니다."
        )

    token_list: list[Token] = Token.query.filter_by(
        project=project.id
    ).all()

    deploy_list: list[Deploy] = Deploy.query.filter_by(
        project=project.id
    ).all()

    return resp(
        payload={
            "token_list": [
                {
                    "owner": x.owner,
                    "created_at": x.created_at.timestamp(),
                    "expired_at": x.expired_at.timestamp(),
                    "last_used_at": x.last_used_at.timestamp()
                }
                for x in token_list
            ],
            "deploy_list": [
                {
                    "owner": x.owner,
                    "created_at": x.created_at.timestamp(),
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
        return resp(
            status=False,
            message="등록된 배포 토큰이 아닙니다."
        )

    if user.id == 1:
        pass
    elif user.id != token.owner:
        return resp(
            status=False,
            message="본인의 배포 토큰만 삭제 할 수 있습니다."
        )

    db.session.delete(token)
    db.session.commit()

    return resp(
        message="배포 토큰이 삭제되었습니다."
    )


@bp.post("/token/test")
def token_test():
    name: str = request.headers.get("x-deploy-name", "")

    if len(name) == 0:
        return resp(
            status=False,
            message="프로젝트 이름이 없습니다."
        )

    match = RE.match(name)

    if match is None:
        return resp(
            status=False,
            message="프로젝트 이름이 올바르지 않습니다."
        )

    token: str = request.headers.get("x-deploy-token", "")

    if len(token) == 0:
        return resp(
            status=False,
            message="배포 토큰이 없습니다."
        )

    project: Project = Project.query.filter_by(
        name=name
    ).first()

    if project is None:
        return resp(
            status=False,
            message="등록된 프로젝트가 아닙니다."
        )

    tk: Token = Token.query.filter_by(
        project=project.id,
        token=token
    ).first()

    if tk is None:
        return resp(
            status=False,
            message="등록된 배포 토큰이 아닙니다."
        )

    tk.last_used_at = datetime.now()
    db.session.commit()

    return resp(
        message="배포 토큰 테스트에 성공했습니다!"
    )
