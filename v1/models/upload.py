from pydantic import BaseModel


class UploadResult(BaseModel):
    """
    Response for upload type deploy request
    """
    result: bool
    reason: str = "no reason"
