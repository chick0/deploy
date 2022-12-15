from os import remove
from re import compile
from shutil import rmtree
from logging import getLogger
from datetime import datetime

from flask import Blueprint
from flask import current_app as app
from flask import request
from flask import flash
from flask import redirect
from flask import url_for
from flask import render_template

from .. import db
from ..models import User
from ..models import Project
from ..models import Token
from ..models import Deploy
from ..user import login_required
from ..utils import get_from
from deploy.path import upload_path_with_deploy_id
from deploy.path import project_path_with_name

bp = Blueprint("project", __name__, url_prefix="/project")
logger = getLogger()

RE = compile(r"^[a-z0-9-._]+$")


@bp.get("/list")
@login_required
def get_list(user: User):
    if user.id == 1:
        project_list = Project.query.all()
    else:
        project_list = Project.query.filter_by(
            owner=user.id
        ).all()

    if len(project_list) == 0:
        flash("등록된 프로젝트가 없습니다.")
        return redirect(url_for("project.create"))

    token_map = {}

    for project_id in [project.id for project in project_list]:
        token_map[project_id] = Token.query.filter_by(
            project=project_id
        ).count()

    return render_template(
        "project/get-list.jinja2",
        project_list=project_list,
        token=token_map
    )


@bp.get("/create")
@login_required
def create(user: User):
    count = Project.query.filter_by(
        owner=user.id
    ).count()

    PROJECT_MAX = app.config['PROJECT_MAX']

    if count > PROJECT_MAX:
        flash(f"{PROJECT_MAX}개보다 많은 프로젝트를 생성할 수 없습니다.")
        return redirect(url_for("project.get_list"))

    return render_template(
        "project/create.jinja2",
        count=count
    )


@bp.post("/create")
@login_required
def create_post(user: User):
    name = request.form.get("name", "")

    if len(name) < 4:
        flash("프로젝트 이름은 4글자보다 길어야합니다.", "project.create")
        return redirect(url_for("project.create"))

    if len(name) > 100:
        flash("프로젝트 이름은 100글자보다 짧아야합니다.", "project.create")
        return redirect(url_for("project.create"))

    if name.startswith("."):
        flash("프로젝트 이름은 '.'으로 시작할 수 없습니다!", "project.create")
        return redirect(url_for("project.create"))

    match = RE.match(name)

    if match is None:
        flash("프로젝트 이름은 영어 소문자와 숫자를 포함한 일부 기호(-, _, .)만 사용할 수 있습니다.", "project.create")
        return redirect(url_for("project.create"))

    if Project.query.filter_by(
        name=name
    ).count() != 0:
        flash("이미 사용중인 프로젝트 이름입니다.", "project.create")
        return redirect(url_for("project.create"))

    project = Project()
    project.owner = user.id
    project.name = name
    project.created_at = datetime.now()

    db.session.add(project)
    db.session.commit()

    logger.info(f"({project.id}) {project.name} project is created from {get_from()}")

    return redirect(url_for("project.get_list") + f"#project-{project.id}")


@bp.get("/delete/<int:project_id>")
@login_required
def delete(user: User, project_id: int):
    project: Project = Project.query.with_entities(
        Project.name,
        Project.owner
    ).filter_by(
        id=project_id
    ).first()

    if project is None:
        flash("등록된 프로젝트가 아닙니다.")
        return redirect(url_for("project.get_list"))

    if user.id == 1:
        pass
    elif user.id != project.owner:
        flash("해당 프로젝트를 삭제할 권한이 없습니다.")
        return redirect(url_for("project.get_list"))

    delete_list = []
    delete_list.append(f"<b>{project.name}</b> 프로젝트")

    token_c = Token.query.filter_by(
        project=project_id
    ).count()

    if token_c != 0:
        delete_list.append(f"<b>{token_c}개</b>의 배포 토큰")

    deploy_c = Deploy.query.filter_by(
        project=project_id
    ).count()

    if deploy_c != 0:
        delete_list.append(f"<b>{deploy_c}개</b>의 배포 버전")

    return render_template(
        "project/delete.jinja2",
        delete_list=delete_list
    )


@bp.post("/delete/<int:project_id>")
@login_required
def delete_post(user: User, project_id: int):
    project: Project = Project.query.filter_by(
        id=project_id
    ).first()

    if project is None:
        flash("등록된 프로젝트가 아닙니다.")
        return redirect(url_for("project.get_list"))

    if user.id == 1:
        pass
    elif user.id != project.owner:
        flash("해당 프로젝트를 삭제할 권한이 없습니다.")
        return redirect(url_for("project.get_list"))

    token_d = Token.query.filter_by(
        project=project.id
    ).delete()

    deploy_list: list[Deploy] = Deploy.query.filter_by(
        project=project.id
    ).all()

    for deploy in deploy_list:
        try:
            remove(upload_path_with_deploy_id(deploy.owner, deploy.id))
        except FileNotFoundError:
            pass

        db.session.delete(deploy)

    try:
        rmtree(project_path_with_name(project.name))
    except FileNotFoundError:
        pass

    db.session.delete(project)
    db.session.commit()

    delete_status = f"(token: {token_d}, deploy: {len(deploy_list)})"
    logger.info(f"({project.id}) {project.name} project is deleted {delete_status} from {get_from()}")

    flash(f"<b>{project.name}</b> 프로젝트가 삭제되었습니다.", "success")
    return redirect(url_for("project.get_list"))
