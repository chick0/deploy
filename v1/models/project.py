from pydantic import BaseModel


class ProjectCreate(BaseModel):
    title: str
    owner: str


class Project(BaseModel):
    uuid: str
    title: str
    owner: str


class ProjectList(BaseModel):
    projectList: list[Project]


class ProjectUpdateResult(BaseModel):
    result: bool
    reason: str = "no reason"
