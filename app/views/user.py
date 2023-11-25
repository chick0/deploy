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
from ..models import Token
from ..models import Deploy
from ..user import login_required
from ..utils import get_from
from ..utils import logout
from ..tools import get_g_cache
from ..tools import set_g_cache
from deploy import UPLOAD_DIR
from deploy import create_dir
from deploy.remove import remove_user_path_with_user_id
from deploy.remove import remove_upload_path_with_deploy_id
from deploy.remove import remove_unzip_path_with_deploy_id
from deploy.remove import remove_project_path_with_name

bp = Blueprint("user", __name__, url_prefix="/user")
logger = getLogger()


@bp.get("/dashboard")
@login_required
def dashboard(user: User):
    p_count = Project.query.filter(
        Project.owner == user.id
    ).count()

    d_count = Deploy.query.filter(
        Deploy.owner == user.id
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

    logger.info(f"User id {user.id} change password from {get_from()}")
    return redirect(url_for("user.dashboard"))


@bp.get("/clean-up")
@login_required
def clean_up(user: User):
    count = 0

    for deploy in Deploy.query.filter(
        Deploy.owner == user.id,
    ).all():
        key = f"project.{deploy.project}.last_deploy"
        using_id = get_g_cache(key)

        if using_id is None:
            project = Project.query.with_entities(
                Project.last_deploy,
            ).filter(
                Project.id == deploy.project,
            ).first()

            if project is None:
                raise ValueError("등록된 프로젝트가 아닙니다.")

            using_id = project.last_deploy
            set_g_cache(key, using_id)

        if deploy.id != using_id:
            remove_upload_path_with_deploy_id(user.id, deploy.id)
            logger.info(f"Deploy id {deploy.id} is deleted by {user.id} from {get_from()}")

            db.session.delete(deploy)
            count += 1

    db.session.commit()

    flash(f"<b>{count}개</b>의 미사용 버전이 삭제되었습니다.", "success")
    return redirect(url_for("user.dashboard"))


@bp.get("/delete")
@login_required
def delete(user: User):
    if user.id == 1:
        try:
            user_id = int(request.args.get("user_id", "a"))

            db_user = User.query.filter(
                User.id == user_id
            ).first()

            if db_user is None:
                flash("등록된 계정이 아닙니다.")
                return redirect(url_for("user.dashboard"))
        except ValueError:
            pass

    if user.id == 1:
        flash("관리자 계정은 삭제할 수 없습니다.")
        return redirect(url_for("user.dashboard"))

    delete_list = []
    delete_list.append(f"<b>{user.email}</b> 계정")

    token_c = Token.query.filter(
        Token.owner == user.id
    ).count()

    if token_c != 0:
        delete_list.append(f"<b>{token_c}개+</b>의 배포 토큰")

    deploy_c = Deploy.query.filter(
        Deploy.owner == user.id
    ).count()

    if deploy_c != 0:
        delete_list.append(f"<b>{deploy_c}개+</b>의 배포 버전")

    project_list: list[Project] = Project.query.filter(
        Deploy.owner == user.id
    ).all()

    for project in project_list:
        delete_list.append(f"<b>{project.name}</b> 프로젝트")

    return render_template(
        "user/delete.jinja2",
        delete_list=delete_list
    )


@bp.post("/delete")
@login_required
def delete_post(user: User):
    by_admin = False

    if user.id == 1:
        try:
            by_admin = True
            user_id = int(request.args.get("user_id", "a"))

            db_user = User.query.filter(
                User.id == user_id
            ).first()

            if db_user is None:
                flash("등록된 계정이 아닙니다.")
                return redirect(url_for("user.dashboard"))
        except ValueError:
            pass

    if user.id == 1:
        flash("관리자 계정은 삭제할 수 없습니다.")
        return redirect(url_for("user.dashboard"))

    for token in Token.query.filter(
        Token.owner == user.id
    ).all():
        db.session.delete(token)

    for deploy in Deploy.query.filter(
        Deploy.owner == user.id
    ).all():
        db.session.delete(deploy)

    remove_user_path_with_user_id(user.id)

    for project in Project.query.filter(
        Project.owner == user.id
    ).all():
        for token in Token.query.filter(
            Token.project == project.id
        ).all():
            db.session.delete(token)

        for deploy in Deploy.query.filter(
            Deploy.project == project.id
        ).all():
            remove_upload_path_with_deploy_id(deploy.owner, deploy.id)
            remove_unzip_path_with_deploy_id(deploy.id)
            db.session.delete(deploy)

        remove_project_path_with_name(project.name)
        db.session.delete(project)

    db.session.delete(user)
    db.session.commit()

    if by_admin:
        logger.info(f"User id {user.id} is deleted by admin from {get_from()}")

        flash("계정이 삭제되었습니다.", "success")
        return redirect(url_for("admin.user_list"))
    else:
        logger.info(f"User id {user.id} is deleted from {get_from()}")

        return logout("계정이 삭제되었습니다.", "success")
