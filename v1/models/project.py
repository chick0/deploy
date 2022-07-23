from pydantic import BaseModel


class ProjectCreate(BaseModel):
    """
    Payload for create Project
    """
    title: str
    type: int
    path: str
    command: str


class Project(BaseModel):
    """
    Payload for read/write Project
    """
    uuid: str
    title: str
    owner: str
    type: int
    path: str
    command: str


class ProjectUpdateResult(BaseModel):
    """
    Response for Project update
    """
    result: bool
    reason: str = "no reason"
