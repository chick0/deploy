from typing import Union

from pydantic import BaseModel


class PullResult(BaseModel):
    """
    Response for pull type deploy request
    """
    result: bool
    reason: str = "no reason"
    log: Union[int, None] = None
