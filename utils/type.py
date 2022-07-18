from enum import Enum


class ProjectType(Enum):
    """
    Type for Project.
    """
    FRONTEND = 0
    BACKEND = 1
    BOT = 2


def verify_type(project_type: int) -> bool:
    """
    Verify project type is correct

    :param project_type: project type for test
    :return: verify result
    """
    return any(
        [
            getattr(ProjectType, x).value == project_type
            for x in dir(ProjectType)
            if isinstance(getattr(ProjectType, x), ProjectType)
        ]
    )
