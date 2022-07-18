from pydantic import BaseModel


class PullResult(BaseModel):
    """
    Response for pull type deploy request
    """
    result: bool
    reason: str = "no reason"
