from os import stat
from os import listdir
from os.path import join
from hashlib import sha512
from logging import getLogger
from datetime import datetime

from flask import Blueprint
from flask import current_app as app
from flask import request
from flask import flash
from flask import render_template
from flask import redirect
from flask import url_for

from .. import db
from ..models import User
from ..models import Project
from ..models import Deploy
from ..user import login_required
from ..utils import get_from
from deploy import UPLOAD_DIR
from deploy import create_dir

bp = Blueprint("user", __name__, url_prefix="/user")
logger = getLogger()


@bp.get("/dashboard")
@login_required
def dashboard(user: User):
    p_count = Project.query.filter_by(
        owner=user.id
    ).count()

    d_count = Deploy.query.filter_by(
        owner=user.id
    ).count()

    PATH: str = join(UPLOAD_DIR, str(user.id))
    create_dir(PATH)

    using_size = 0
    for file in listdir(PATH):
        using_size += stat(join(PATH, file)).st_size

    return render_template(
        "user/dashboard.jinja2",
        user=user,
        using_size=using_size,
        p_count_per=int(p_count / app.config['PROJECT_MAX'] * 100),
        d_count_per=int(d_count / app.config['DEPLOY_MAX'] * 100)
    )


@bp.get("/password-update")
@login_required
def password_update(user: User):
    return render_template(
        "user/password-update.jinja2",
    )


@bp.post("/password-update")
@login_required
def password_update_post(user: User):
    old_password = sha512(request.form.get("old-password", "").encode()).hexdigest()

    if user.password != old_password:
        flash("기존 비밀번호가 일치하지 않습니다.", "user-password-update")
        return redirect(url_for("user.password_update"))

    password = request.form.get("password", "")

    if len(password) < 12:
        flash("12글자 이상으로 긴 비밀번호를 입력해야합니다.", "user-password-update")
        return redirect(url_for("user.password_update"))

    if password != request.form.get("password-check", ""):
        flash("비밀번호가 일치하지 않습니다. 다시 한 번 확인해주세요.", "user-password-update")
        return redirect(url_for("user.password_update"))

    new_password = sha512(password.encode()).hexdigest()

    if new_password == user.password:
        flash("동일한 비밀번호로 변경할 수 없습니다.", "user-password-update")
        return redirect(url_for("user.password_update"))

    user.password = new_password
    user.password_updated_at = datetime.now()
    db.session.commit()

    logger.info(f"({user.id}) {user.email} user update password from {get_from()}")

    return redirect(url_for("user.dashboard"))
