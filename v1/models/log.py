from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class LogID(BaseModel):
    """
    Deploy Log ID or Metadata
    """
    id: int
    create_by: str
    type: int
    created_at: datetime
    return_code: int


class LogIDList(BaseModel):
    """
    List of Log ID
    """
    logIDList: list[LogID]


class LogItem(BaseModel):
    """
    deploy log item without child
    """
    id: int
    create_by: str

    # utils.type.DeployLogType
    type: int

    created_at: datetime

    return_code: int
    stdout: str
    stderr: str


class Log(LogItem):
    """
    Response models for deploy log
    """
    # when pull log (->command log)
    child: Optional[LogItem] = None
