from pydantic import BaseModel

from .project import Project


class ProjectList(BaseModel):
    projectList: list[Project]
