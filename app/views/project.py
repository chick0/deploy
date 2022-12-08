from logging import getLogger

from flask import Blueprint
from flask import render_template

from ..user import login_required

bp = Blueprint("project", __name__, url_prefix="/project")
logger = getLogger()


@bp.get("/list")
@login_required
def get_list(user):
    return render_template(
        "project/get-list.jinja2"
    )
