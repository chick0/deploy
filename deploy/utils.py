from os import rename
from typing import NamedTuple
from datetime import datetime
from functools import wraps
from zipfile import ZipFile

from flask import request

from app import db
from app.models import Project
from app.models import Token
from app.models import Deploy
from app.utils import response
from app.views.project import RE
from . import create_dir
from .path import upload_path_with_deploy_id
from .path import unzip_path_with_deploy_id
from .path import project_path_with_name
from .remove import remove_project_path_with_name


class GetSavePathResponse(NamedTuple):
    path: str
    deploy: Deploy


def auth_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        name: str = request.headers.get("x-deploy-name", "")

        if len(name) == 0:
            return response(
                status=False,
                message="프로젝트 이름이 없습니다."
            )

        match = RE.match(name)

        if match is None:
            return response(
                status=False,
                message="프로젝트 이름이 올바르지 않습니다."
            )

        ########################################################

        token: str = request.headers.get("x-deploy-token", "")

        if len(token) == 0:
            return response(
                status=False,
                message="배포 토큰이 없습니다."
            )

        ########################################################

        project: Project = Project.query.filter_by(
            name=name
        ).first()

        if project is None:
            return response(
                status=False,
                message="등록된 프로젝트가 아닙니다."
            )

        ########################################################

        tk: Token = Token.query.filter_by(
            project=project.id,
            token=token
        ).first()

        if tk is None:
            return response(
                status=False,
                message="등록된 배포 토큰이 아닙니다."
            )

        ########################################################

        if tk.owner == 1:
            pass
        elif tk.owner != project.owner:
            return response(
                status=False,
                message="해당 프로젝트에 접근할 권한이 없습니다."
            )

        kwargs['project'] = project
        kwargs['token'] = tk
        return f(*args, **kwargs)

    return decorator


def get_save_path(token: Token) -> GetSavePathResponse:
    deploy = Deploy()
    deploy.owner = token.owner
    deploy.project = token.project
    deploy.created_at = datetime.now()

    db.session.add(deploy)
    db.session.commit()

    return GetSavePathResponse(
        deploy=deploy,
        path=upload_path_with_deploy_id(token.owner, deploy.id)
    )


def unzip_uploaded(user_id: int, deploy_id: int):
    path = upload_path_with_deploy_id(user_id, deploy_id)
    output = unzip_path_with_deploy_id(deploy_id)
    create_dir(output)

    with ZipFile(file=path) as zip:
        for member in zip.infolist():
            member.filename = fix_zip_filename(member.filename)
            zip.extract(member, output)


def set_project_deploy(deploy_id: int, name: str):
    unzip_path = unzip_path_with_deploy_id(deploy_id)
    project_path = project_path_with_name(name)

    remove_project_path_with_name(name)
    rename(unzip_path, project_path)


def fix_zip_filename(filename: str) -> str:
    return filename.encode("cp437").decode("cp949").encode("utf-8").decode("utf-8")
