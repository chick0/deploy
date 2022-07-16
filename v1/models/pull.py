from pydantic import BaseModel


class PullResult(BaseModel):
    result: bool
    reason: str = "no reason"
