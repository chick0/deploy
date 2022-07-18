from datetime import datetime
from subprocess import run

from fastapi import APIRouter
from fastapi import Depends

from sql import get_session
from sql.models import Project
from sql.models import DeployLog
from v1.const import deploy
from v1.models.pull import PullResult
from utils.token.deploy import parse_token
from utils.type import ProjectType
from utils.type import DeployLogType

router = APIRouter(
    tags=["Pull"]
)


@router.post(
    "/pull",
    description="소스코드의 변경 사항을 적용합니다.",
    response_model=PullResult
)
# pylint: disable=missing-function-docstring
async def pull_and_deploy(token=Depends(deploy)):
    payload = parse_token(token=token)
    if not payload.permission.write:
        return PullResult(
            result=False,
            reason="쓰기 권한이 없어 해당 토큰을 사용 할 수 없습니다."
        )

    session = get_session()
    project: Project = session.query(Project).filter_by(
        uuid=payload.project
    ).first()

    if project is None:
        session.close()
        return PullResult(
            result=False,
            reason="등록된 프로젝트가 아닙니다."
        )

    if project.type == ProjectType.FRONTEND.value:
        session.close()
        return PullResult(
            result=False,
            reason="프론트 프로젝트는 해당 방식으로 배포 할 수 없습니다."
        )

    pull_output = run(
        "git pull",
        capture_output=True,
        cwd=project.path,
        check=False
    )

    pull_log = DeployLog()
    pull_log.project = project.uuid
    pull_log.create_by = payload.user
    pull_log.type = DeployLogType.PULL.value
    # pull_log.called_by = not here
    pull_log.created_at = datetime.now()

    pull_log.return_code = pull_output.returncode
    pull_log.stdout = pull_output.stdout.decode()
    pull_log.stderr = pull_output.stderr.decode()

    session.add(pull_log)
    session.commit()

    if pull_output.returncode != 0:
        try:
            return PullResult(
                result=False,
                reason="pull 과정에서 오류가 발생했습니다.",
                log=pull_log.id
            )
        finally:
            session.close()

    if len(project.command) != 0:
        command_output = run(
            project.command,
            capture_output=True,
            cwd=project.path
        )

        command_log = DeployLog()
        command_log.project = project.uuid
        command_log.create_by = payload.user
        command_log.type = DeployLogType.COMMAND.value
        command_log.called_by = pull_log.id
        command_log.created_at = pull_log.created_at

        command_log.return_code = command_output.returncode
        command_log.stdout = command_output.stdout.decode()
        command_log.stderr = command_output.stderr.decode()

        session.add(command_output)
        session.commit()

        if command_output.returncode != 0:
            try:
                return PullResult(
                    result=False,
                    reason="재시작 명령 실행 과정에서 오류가 발생했습니다.",
                    log=command_log.id
                )
            finally:
                session.close()

    try:
        return PullResult(
            result=True,
        )
    finally:
        session.close()
