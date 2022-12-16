from flask import Blueprint
from flask import flash
from flask import redirect
from flask import url_for

from ..user import login_not_required

bp = Blueprint("index", __name__, url_prefix="/")


@bp.get("")
@login_not_required
def index():
    flash("로그인이 필요합니다.")
    return redirect(url_for("auth.login"))
