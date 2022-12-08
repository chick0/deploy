from hashlib import sha512
from logging import getLogger
from datetime import datetime

from flask import Blueprint
from flask import request
from flask import session
from flask import redirect
from flask import url_for
from flask import render_template
from flask import flash

from .. import db
from ..models import User
from ..utils import get_from
from ..user import login_not_required

bp = Blueprint("auth", __name__, url_prefix="/auth")
logger = getLogger()


@bp.get("/logout")
def logout():
    for key in list(session.keys()):
        del session[key]

    return redirect(url_for("index.index"))


@bp.get("/login")
@login_not_required
def login():
    return render_template(
        "auth/login.jinja2"
    )


@bp.post("/login")
@login_not_required
def login_post():
    fail_message = "Login failed cause {0}. And request from " + get_from()

    email = request.form.get("email", "")

    if len(email) == 0:
        logger.info(fail_message.format("email is empty"))

        flash("이메일을 입력해야합니다.", "login")
        return redirect(url_for("auth.login"))

    password = request.form.get("password", "")

    if len(password) == 0:
        logger.info(fail_message.format("password is empty"))

        flash("비밀번호를 입력해야합니다.", "login")
        return redirect(url_for("auth.login"))

    user: User = User.query.filter_by(
        email=email.strip(),
        password=sha512(password.encode()).hexdigest()
    ).first()

    if user is None:
        logger.info(fail_message.format("not registered user"))

        flash("등록된 계정이 아닙니다.", "login")
        return redirect(url_for("auth.login"))

    if user.password_updated_at is None:
        session['tmp+user.id'] = user.id
        session['tmp+user.email'] = user.email
        return redirect(url_for("auth.password_update"))

    session['user.id'] = user.id
    session['user.password'] = user.password

    user.last_login_at = datetime.now()
    db.session.commit()

    return redirect(url_for("project.get_list"))


@bp.get("/password-update")
@login_not_required
def password_update():
    try:
        return render_template(
            "auth/password-update.jinja2",
            email=session['tmp+user.email']
        )
    except KeyError:
        flash("로그인이 필요합니다.")
        return redirect(url_for("auth.login"))


@bp.post("/password-update")
@login_not_required
def password_update_post():
    try:
        user_id = session['tmp+user.id']
        email = session['tmp+user.email']
    except KeyError:
        flash("로그인이 필요합니다.")
        return redirect(url_for("auth.login"))

    user: User = User.query.filter_by(
        id=user_id,
        email=email
    ).first()

    password = request.form.get("password", "")

    if len(password) < 12:
        flash("12글자 이상으로 긴 비밀번호를 입력해야합니다.", "password-update")
        return redirect(url_for("auth.password_update"))

    if password != request.form.get("password-check", ""):
        flash("비밀번호가 일치하지 않습니다. 다시 한 번 확인해주세요.", "password-update")
        return redirect(url_for("auth.password_update"))

    user.password = sha512(password.encode()).hexdigest()
    user.last_login_at = datetime.now()
    user.password_updated_at = datetime.now()
    db.session.commit()

    session['user.id'] = user.id
    session['user.password'] = user.password

    del session['tmp+user.id']
    del session['tmp+user.email']

    return redirect(url_for("project.get_list"))
