from functools import wraps
from typing import Optional

from flask import session
from flask import flash
from flask import url_for

from .error import RedirectRequired
from .models import User


def get_user(user_id: int) -> Optional[User]:
    return User.query.filter_by(
        id=user_id,
    ).first()


def login_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        try:
            user_id = session['user.id']
            user_password = session['user.password']
        except KeyError:
            flash("로그인이 필요합니다.")
            raise RedirectRequired(url_for("auth.logout"))

        user = get_user(user_id)

        if user is None:
            flash("삭제된 계정입니다.")
            raise RedirectRequired(url_for("auth.logout"))

        if user.password != user_password:
            flash("비밀번호가 변경되었습니다. 다시 로그인해주세요.")
            raise RedirectRequired(url_for("auth.logout"))

        return f(*args, **kwargs, user=user)

    return decorator


def login_not_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        try:
            user_id = session['user.id']
            user_password = session['user.password']
        except KeyError:
            return f(*args, **kwargs)

        user = get_user(user_id)

        if user is None or user.password != user_password:
            return f(*args, **kwargs)

        raise RedirectRequired(url_for("project.get_list"))

    return decorator
