from secrets import token_bytes
from datetime import datetime

from flask import Blueprint
from flask import request
from flask import flash
from flask import redirect
from flask import url_for
from flask import render_template

from .. import db
from ..models import User
from ..models import Project
from ..models import Token
from ..user import login_required

bp = Blueprint("token", __name__, url_prefix="/token")


@bp.get("/list")
@login_required
def get_list(user: User):
    token_list: list[Token] = Token.query.filter_by(
        owner=user.id
    ).all()

    if len(token_list) == 0:
        return redirect(url_for("token.create"))

    return render_template(
        "token/get-list.jinja2",
        token_list=token_list
    )


@bp.get("/create")
@login_required
def create(user: User):
    project_list: list[Project] = Project.query.filter_by(
        owner=user.id
    ).all()

    return render_template(
        "token/create.jinja2",
        project_list=project_list
    )


@bp.post("/create")
@login_required
def create_post(user: User):
    try:
        project_id = int(request.form.get("project_id", None))  # type: ignore
    except (TypeError, ValueError):
        flash("프로젝트 아이디가 올바르지 않습니다.", "token-create")
        return redirect(url_for("token.create"))

    expired_at = request.form.get("expired_at", None)

    if expired_at is not None:
        try:
            expired_at = datetime.strptime(expired_at, "%Y-%m-%d")
        except ValueError:
            flash("배포 토큰 만료 날짜가 올바르지 않습니다.", "token-create")
            return redirect(url_for("token.create"))

    project: Project = Project.query.with_entities(
        Project.id,
        Project.owner
    ).filter_by(
        id=project_id
    ).first()

    if user.id == 1:
        pass
    elif user.id != project.owner:
        flash("배포 토큰을 생성할 권한이 없습니다.", "token-create")
        return redirect(url_for("token.create"))

    if expired_at is None:
        token_length = 48  # 96
    else:
        token_length = 32  # 32

    token = token_bytes(token_length).hex()

    tk = Token()
    tk.owner = user.id
    tk.project = project.id
    tk.created_at = datetime.now()
    tk.expired_at = expired_at
    tk.last_used_at = None
    tk.token = token

    db.session.add(tk)
    db.session.commit()

    return render_template(
        "token/create-post.jinja2",
        project_id=project.id,
        expired_at=expired_at,
        token=token
    )


@bp.get("/test")
def test():
    return render_template(
        "token/test.jinja2"
    )
