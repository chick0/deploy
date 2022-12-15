from functools import wraps

from flask import current_app as app
from flask import flash
from flask import redirect
from flask import url_for

from .models import User
from .models import Project
from .models import Token
from .models import Deploy
from .utils import response


def check_project_max(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        user: User = kwargs['user']

        count = Project.query.filter_by(
            owner=user.id
        ).count()

        PROJECT_MAX = app.config['PROJECT_MAX']

        if count >= PROJECT_MAX:
            flash(f"{PROJECT_MAX}개보다 많은 프로젝트를 생성할 수 없습니다.")
            return redirect(url_for("project.get_list"))

        return f(*args, **kwargs)

    return decorator


def check_deploy_max(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        project: Project = kwargs['project']
        token: Token = kwargs['token']

        count = Deploy.query.filter_by(
            owner=token.owner,
            project=project.id,
        ).count()

        DEPLOY_MAX = app.config['DEPLOY_MAX']

        if count >= DEPLOY_MAX:
            return response(
                status=False,
                message=f"{DEPLOY_MAX}개보다 많은 버전을 등록할 수 없습니다.",
            )

        return f(*args, **kwargs)

    return decorator
