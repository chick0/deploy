from hashlib import sha512
from logging import getLogger
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
from ..user import login_required
from ..utils import get_from

bp = Blueprint("admin", __name__, url_prefix="/admin")
logger = getLogger()

project_list = "project.get_list"


@bp.get("/user-list")
@login_required
def user_list(user: User):
    if user.id != 1:
        flash("계정 목록은 관리자만 사용할 수 있습니다.")
        return redirect(url_for(project_list))

    user_list: list[User] = User.query.all()

    return render_template(
        "admin/user-list.jinja2",
        user_list=user_list
    )


@bp.get("/user-add")
@login_required
def user_add(user: User):
    if user.id != 1:
        flash("계정 등록은 관리자만 할 수 있습니다.")
        return redirect(url_for(project_list))

    return render_template(
        "admin/user-add.jinja2"
    )


@bp.post("/user-add")
@login_required
def user_add_post(user: User):
    if user.id != 1:
        flash("계정 등록은 관리자만 할 수 있습니다.")
        return redirect(url_for(project_list))

    email = request.form.get("email", "").strip()

    if len(email) == 0 or email.find("@") == -1:
        flash("입력한 이메일이 올바르지 않습니다.", "user-add")
        return redirect(url_for("admin.user_add"))

    if User.query.filter(
        User.email == email
    ).count() != 0:
        flash("사용중인 이메일입니다.", "user-add")
        return redirect(url_for("admin.user_add"))

    password = token_bytes(16).hex()

    new_user = User()
    new_user.email = email
    new_user.password = sha512(password.encode()).hexdigest()
    new_user.created_at = datetime.now()

    db.session.add(new_user)
    db.session.commit()

    logger.info(f"New user id {new_user.id} and email {new_user.email} is added from {get_from()}")

    return render_template(
        "admin/user-add-post.jinja2",
        email=email,
        password=password,
    )


@bp.get("/password-reset/<int:user_id>")
@login_required
def password_reset(user_id: int, user: User):
    if user.id != 1:
        flash("임시 비밀번호 설정은 관리자만 할 수 있습니다.")
        return redirect(url_for(project_list))

    target = User.query.filter(
        User.id == user_id
    ).first()

    if target is None:
        flash("등록된 사용자가 아닙니다.")
        return redirect(url_for(project_list))

    password = token_bytes(16).hex()

    target.password = sha512(password.encode()).hexdigest()
    target.password_updated_at = None

    db.session.commit()

    logger.info(f"Admin set user id {target.id} password to temp password from {get_from()}")

    return render_template(
        "admin/password-reset.jinja2",
        user_id=target.id,
        email=target.email,
        password=password
    )
