from pydantic import BaseModel


class TokenRequest(BaseModel):
    """
    Payload for create deploy token
    """
    project: str
    permission: list[str]


class TokenResponse(BaseModel):
    """
    Response for create deploy token
    """
    token: str


class TokenDelete(BaseModel):
    """
    Payload for delete deploy token
    """
    uuid: str


class TokenDeleteResult(BaseModel):
    """
    Response for delete deploy token
    """
    result: bool
    reason: str = "no reason"
