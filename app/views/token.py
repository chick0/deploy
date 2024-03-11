from hashlib import sha384
from secrets import token_bytes
from logging import getLogger
from datetime import datetime

from flask import Blueprint
from flask import request
from flask import render_template

from .. import db
from ..models import User
from ..models import Project
from ..models import Token
from ..const import TOKEN_MAX
from ..user import login_required
from ..utils import get_from

bp = Blueprint("token", __name__, url_prefix="/token")
logger = getLogger()


@bp.get("/create/<string:name>")
@login_required
def create(user: User, name: str):
    if user.id == 1:
        project = Project.query.filter(
            Project.name == name
        ).first()
    else:
        project = Project.query.filter(
            Project.owner == user.id,
            Project.name == name
        ).all()

    if project is None:
        return "등록된 프로젝트가 아닙니다.", 404

    return render_template(
        "token/create.jinja2",
        name=name
    )


@bp.post("/create")
@login_required
def create_post(user: User):
    name = request.form.get("name", None)

    if name is None:
        return "필수 데이터가 누락되었습니다.", 400

    expired_at = request.form.get("expired_at", None)

    if user.id == 1:
        project = Project.query.filter(
            Project.name == name
        ).first()
    else:
        project = Project.query.filter(
            Project.owner == user.id,
            Project.name == name,
        ).first()

    if project is None:
        return "등록된 프로젝트가 아니거나 권한이 없습니다.", 404

    token_count = Token.query.filter(
        Token.project == project.id
    ).count()

    if token_count >= TOKEN_MAX:
        return "프로젝트당 최대 10개의 배포 토큰을 생성할 수 있습니다.", 400

    if expired_at is not None:
        try:
            expired_at = datetime.strptime(expired_at, "%Y-%m-%d %H:%M")
        except ValueError:
            return "배포 토큰 만료 날짜가 올바르지 않습니다.", 400

    if expired_at is None:
        token_length = 48  # 96
    else:
        token_length = 32  # 32

    raw = token_bytes(token_length)
    token = sha384(raw).hexdigest()

    tk = Token()
    tk.owner = user.id
    tk.project = project.id
    tk.created_at = datetime.now()
    tk.expired_at = expired_at
    tk.last_used_at = None
    tk.token = token

    db.session.add(tk)
    db.session.commit()

    logger.info(f"Deploy token id {tk.id}, owner {tk.owner}, project {tk.project} is created from {get_from()}")

    return raw.hex(), 201


@bp.delete("/<int:token_id>")
@login_required
def delete(user: User, token_id: int):
    if user.id == 1:
        result = Token.query.filter(
            Token.id == token_id
        ).delete()
    else:
        result = Token.query.filter(
            Token.id == token_id,
            Token.owner == user.id
        ).delete()

    if result == 1:
        db.session.commit()
        return "해당 배포 토큰이 삭제되었습니다.", 200

    if user.id == 1:
        return "배포 토큰 삭제에 실패했습니다. 등록된 토큰이 아닙니다.", 404

    return "배포 토큰 삭제에 실패했습니다. 권한이 없거나 등록된 토큰이 아닙니다.", 400
