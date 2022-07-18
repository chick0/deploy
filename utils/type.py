from enum import Enum


class ProjectType(Enum):
    FRONTEND = 0
    BACKEND = 1
    BOT = 2


def verify_type(project_type: int):
    return any(
        [
            getattr(ProjectType, x).value == project_type
            for x in dir(ProjectType)
            if isinstance(getattr(ProjectType, x), ProjectType)
        ]
    )
