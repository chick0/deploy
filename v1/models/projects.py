from pydantic import BaseModel

from .project import Project


class ProjectList(BaseModel):
    """
    Model for show Projects list
    """
    projectList: list[Project]
