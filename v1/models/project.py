from pydantic import BaseModel


class ProjectCreate(BaseModel):
    title: str
    type: int
    path: str


class Project(BaseModel):
    uuid: str
    title: str
    owner: str
    type: int
    path: str


class ProjectList(BaseModel):
    projectList: list[Project]


class ProjectUpdateResult(BaseModel):
    result: bool
    reason: str = "no reason"
