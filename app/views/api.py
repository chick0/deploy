from typing import Optional

from flask import Blueprint

# from .. import db
from ..models import User
from ..models import Project
from ..models import Token
from ..models import Deploy
from ..user import login_required

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
        owner=user.id,
        project=project.id
    ).all()

    deploy_list: list[Deploy] = Deploy.query.filter_by(
        owner=user.id,
        project=project.id,
    ).all()

    return resp(
        payload={
            "token_list": [
                {
                    "created_at": x.created_at.timestamp(),
                    "expired_at": x.expired_at.timestamp(),
                    "last_used_at": x.last_used_at.timestamp()
                }
                for x in token_list
            ],
            "deploy_list": [
                {
                    "created_at": x.created_at.timestamp(),
                }
                for x in deploy_list
            ]
        }
    )
