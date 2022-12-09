from hashlib import sha512
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

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.get("/user-list")
@login_required
def user_list(user: User):
    if user.id != 1:
        flash("관리자만 사용할 수 있습니다.")
        return redirect(url_for("project.get_list"))

    user_list: list[User] = User.query.all()

    return render_template(
        "admin/user-list.jinja2",
        user_list=user_list
    )


@bp.get("/user-add")
@login_required
def user_add(user: User):
    if user.id != 1:
        flash("관리자만 사용할 수 있습니다.")
        return redirect(url_for("project.get_list"))

    return render_template(
        "admin/user-add.jinja2"
    )


@bp.post("/user-add")
@login_required
def user_add_post(user: User):
    if user.id != 1:
        flash("관리자만 사용할 수 있습니다.")
        return redirect(url_for("project.get_list"))

    email = request.form.get("email", "").strip()

    if len(email) == 0 or email.find("@") == -1:
        flash("입력한 이메일이 올바르지 않습니다.", "user-add")
        return redirect(url_for("admin.user_add"))

    if User.query.filter_by(
        email=email
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

    return render_template(
        "admin/user-add-post.jinja2",
        email=email,
        password=password,
    )


@bp.get("/password-reset/<int:user_id>")
@login_required
def password_reset(user_id: int, user: User):
    if user.id != 1:
        flash("관리자만 사용할 수 있습니다.")
        return redirect(url_for("project.get_list"))

    target: User = User.query.filter_by(
        id=user_id
    ).first()

    password = token_bytes(16).hex()

    target.password = sha512(password.encode()).hexdigest()
    target.password_updated_at = None

    db.session.commit()

    return render_template(
        "admin/password-reset.jinja2",
        email=target.email,
        password=password
    )
