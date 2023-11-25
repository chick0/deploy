from functools import wraps

from flask import flash
from flask import redirect
from flask import url_for

from .models import User
from .models import Project
from .models import Token
from .models import Deploy
from .const import PROJECT_MAX
from .const import DEPLOY_MAX
from .utils import response


def check_project_max(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        user: User = kwargs['user']

        count: int = Project.query.filter(
            Project.owner == user.id
        ).count()

        if count >= PROJECT_MAX:
            flash(f"{PROJECT_MAX}개보다 많은 프로젝트를 생성할 수 없습니다.")
            return redirect(url_for("projects.show"))

        return f(*args, **kwargs)

    return decorator


def check_deploy_max(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        project: Project = kwargs['project']
        token: Token = kwargs['token']

        count = Deploy.query.filter(
            Deploy.owner == token.owner,
            Deploy.project == project.id,
        ).count()

        if count >= DEPLOY_MAX:
            return response(
                status=False,
                message=f"{DEPLOY_MAX}개보다 많은 버전을 등록할 수 없습니다.",
            )

        return f(*args, **kwargs)

    return decorator
