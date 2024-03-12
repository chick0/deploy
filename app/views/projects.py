from re import compile
from math import trunc
from logging import getLogger
from datetime import datetime

from flask import Blueprint
from flask import request
from flask import abort
from flask import flash
from flask import redirect
from flask import url_for
from flask import render_template
from sqlalchemy import and_

from .. import db
from ..models import User
from ..models import Project
from ..models import Token
from ..models import Deploy
from ..const import PAGE_PER_OBJECT
from ..const import DEPLOY_MAX
from ..const import TOKEN_MAX
from ..user import login_required
from ..max import check_project_max
from ..utils import get_from
from ..utils import get_page
from ..utils import get_size

bp = Blueprint("projects", __name__, url_prefix="/projects")
logger = getLogger()

RE = compile(r"^[a-z0-9-._]+$")


@bp.get("")
@login_required
def show(user: User):
    if user.id == 1:
        filter = and_(Project.id >= 1)
    else:
        filter = and_(Project.owner == user.id)

    project_count = Project.query.filter(filter).count()

    max_page = trunc(project_count / PAGE_PER_OBJECT)
    page = get_page()

    if page > max_page:
        page = max_page

    project_list = Project.query.join(
        User,
        User.id == Project.owner
    ).outerjoin(
        Deploy,
        Deploy.id == Project.last_deploy
    ).filter(
        filter
    ).with_entities(
        Project.id,
        Project.name,
        User.email,
        Deploy.created_at.label("deployed_at"),
    ).offset(
        page * PAGE_PER_OBJECT
    ).limit(
        PAGE_PER_OBJECT
    ).all()

    if len(project_list) == 0:
        flash("등록된 프로젝트가 없습니다.")
        return redirect(url_for("projects.create"))

    return render_template(
        "projects/show.jinja2",
        project_count=project_count,
        project_list=project_list,

        page=page,
        max_page=max_page
    )


@bp.get("/create")
@login_required
@check_project_max
def create(user: User):
    return render_template(
        "projects/create.jinja2"
    )


@bp.post("/create")
@login_required
@check_project_max
def create_post(user: User):
    name = request.form.get("name", "")

    if len(name) < 4:
        flash("프로젝트 이름은 4글자보다 길어야합니다.")
        return redirect(url_for("projects.create"))

    if len(name) > 100:
        flash("프로젝트 이름은 100글자보다 짧아야합니다.")
        return redirect(url_for("projects.create"))

    if name.startswith("."):
        flash("프로젝트 이름은 '.'으로 시작할 수 없습니다!")
        return redirect(url_for("projects.create"))

    match = RE.match(name)

    if match is None:
        flash("프로젝트 이름은 영어 소문자와 숫자를 포함한 일부 기호(-, _, .)만 사용할 수 있습니다.")
        return redirect(url_for("projects.create"))

    if Project.query.filter(
        Project.name == name
    ).count() != 0:
        flash("이미 사용중인 프로젝트 이름입니다.")
        return redirect(url_for("projects.create"))

    project = Project()
    project.owner = user.id
    project.name = name
    project.created_at = datetime.now()

    db.session.add(project)
    db.session.commit()

    logger.info(f"Project id {project.id} and name {project.name} is created from {get_from()}")
    return redirect(url_for("projects.detail", project_id=project.id))


@bp.get("/<int:project_id>/detail")
@login_required
def detail(user: User, project_id: int):
    project = Project.query.join(
        User,
        User.id == Project.owner
    ).filter(
        Project.id == project_id
    ).with_entities(
        User.email,
        Project.owner,
        Project.name,
        Project.created_at,
        Project.last_deploy,
    ).first()

    if project is None:
        abort(404)

    if user.id != 1:  # 관리자 체크
        # 권한 부족
        if project.owner != user.id:
            abort(404)

    version_count = Deploy.query.filter(
        Deploy.project == project_id
    ).count()

    deploy_list = Deploy.query.filter(
        Deploy.project == project_id
    ).all()

    token_list = Token.query.filter(
        Token.project == project_id
    ).all()

    return render_template(
        "projects/detail.jinja2",
        project=project,
        version_count=version_count,

        get_size=get_size,
        deploy_list=deploy_list,
        token_list=token_list,

        DEPLOY_MAX=DEPLOY_MAX,
        TOKEN_MAX=TOKEN_MAX,
    )
