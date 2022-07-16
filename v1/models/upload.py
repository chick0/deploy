from pydantic import BaseModel


class UploadResult(BaseModel):
    result: bool
    reason: str = "no reason"
