from os import remove
from zipfile import ZipFile
from logging import getLogger
from datetime import datetime

from flask import Blueprint
from flask import request

from app import db
from app.utils import response
from app.models import User
from app.models import Project
from app.models import Token
from app.models import Deploy
from app.utils import get_from
from app.user import login_required
from .utils import auth_required
from .utils import get_save_path
from .utils import unzip_uploaded
from .utils import set_project_deploy
from .utils import fix_zip_filename
from .path import upload_path_with_deploy_id

bp = Blueprint("deploy", __name__, url_prefix="/deploy")
logger = getLogger()


@bp.post("/upload")
@auth_required
def upload(project: Project, token: Token):
    if len(request.files) != 1:
        return response(
            status=False,
            message="배포할 파일을 1개 업로드 해야합니다."
        )

    try:
        file = list(request.files.values())[0]
    except KeyError:
        return response(
            status=False,
            message="업로드된 파일이 없습니다."
        )

    token.last_used_at = datetime.now()

    path = get_save_path(token)
    file.save(path.path)
    file.close()

    logger.info(f"({path.deploy.id}) Deploy Status: Saved from {get_from()}")

    project.last_deploy = path.deploy.id

    with open(path.path, mode="rb") as reader:
        head = reader.read(3)

    if head.startswith(b"PK"):
        pass
    else:
        remove(path.path)
        path.deploy.is_success = False
        path.deploy.message = "업로드된 파일이 zip 파일이 아닙니다."

        db.session.commit()
        logger.info(f"({path.deploy.id}) Deploy Status: Fail cause file is not zip file")

        return response(
            status=False,
            message=path.deploy.message
        )

    unzip_uploaded(token.owner, path.deploy.id)
    set_project_deploy(path.deploy.id, project.name)

    path.deploy.is_success = True
    project.last_deploy = path.deploy.id
    db.session.commit()

    logger.info(f"({path.deploy.id}) Deploy Status: Success")

    return response(
        message="파일 업로드가 완료되었습니다.",
    )


@bp.delete("/<int:deploy_id>")
@login_required
def delete(user: User, deploy_id: int):
    deploy: Deploy = Deploy.query.filter_by(
        id=deploy_id
    ).first()

    if deploy is None:
        return response(
            status=False,
            message="등록된 버전이 아닙니다."
        )

    project: Project = Project.query.filter_by(
        id=deploy.project
    ).first()

    if project.last_deploy == deploy.id:
        return response(
            status=False,
            message="사용중인 버전은 삭제할 수 없습니다."
        )

    if user.id == 1:
        pass
    elif deploy.owner == user.id or project.owner == user.id:
        pass
    else:
        return response(
            status=False,
            message="해당 버전을 삭제할 권한이 없습니다."
        )

    try:
        path = upload_path_with_deploy_id(deploy.owner, deploy.id)
        remove(path)
    except FileNotFoundError:
        pass

    db.session.delete(deploy)
    db.session.commit()

    logger.info(f"Deploy id {deploy.id} is deleted by {user.id} from {get_from()}")

    return response(
        message="해당 버전이 삭제되었습니다."
    )


@bp.post("/<int:deploy_id>")
@login_required
def apply(user: User, deploy_id: int):
    deploy: Deploy = Deploy.query.filter_by(
        id=deploy_id
    ).first()

    if deploy is None:
        return response(
            status=False,
            message="등록된 버전이 아닙니다."
        )

    project: Project = Project.query.filter_by(
        id=deploy.project
    ).first()

    if project is None:
        return response(
            status=False,
            message="등록된 버전이 아닙니다."
        )

    if user.id == 1:
        pass
    elif project.owner != user.id:
        return response(
            status=False,
            message="해당 버전을 적용할 권한이 없습니다."
        )

    unzip_uploaded(deploy.owner, deploy.id)
    set_project_deploy(deploy.id, project.name)

    project.last_deploy = deploy.id
    db.session.commit()

    logger.info(f"Deploy id {deploy.id} applied by {user.id} from {get_from()}")

    return response(
        message="버전이 교체되었습니다."
    )


@bp.get("/<int:deploy_id>/tree")
@login_required
def tree(user: User, deploy_id: int):
    deploy: Deploy = Deploy.query.filter_by(
        id=deploy_id
    ).first()

    if deploy is None:
        return response(
            status=False,
            message="등록된 버전이 아닙니다."
        )

    if user.id == 1:
        pass
    elif Token.query.filter_by(
        owner=user.id,
        project=deploy.project
    ).count() == 0:
        return response(
            status=False,
            message="권한이 없습니다."
        )

    path = upload_path_with_deploy_id(deploy.owner, deploy_id)

    members = []
    total_size = 0

    with ZipFile(path, mode="r") as zip:
        for member in zip.infolist():
            filename = fix_zip_filename(member.filename)
            filesize = member.file_size

            if filename != "./" and filename != "/":
                if member.is_dir():
                    filename = filename[:-1]
                else:
                    total_size += filesize

                members.append({
                    "name": filename,
                    "size": filesize,
                    "is_dir": member.is_dir()
                })

    return response(
        payload={
            "members": members,
            "total_size": total_size,
        }
    )
