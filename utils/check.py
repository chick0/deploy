from fastapi import HTTPException

from sql import Session
from sql.models import Project


def check_project(session: Session, uuid: str, user: str) -> Project:
    """
    Check project's owner

    :param session: sqlalchemy orm session
    :param uuid: project uuid
    :param user: user uuid
    :return: project
    """
    project: Project = session.query(Project).filter_by(
        uuid=uuid,
        owner=user
    ).first()

    if project is None:
        session.close()
        raise HTTPException(
            status_code=404,
            detail={
                "msg": "등록된 프로젝트가 아닙니다."
            }
        )

    return project
