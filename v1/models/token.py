from pydantic import BaseModel


class TokenRequest(BaseModel):
    project: str
    permission: list[str]


class TokenResponse(BaseModel):
    token: str


class TokenDelete(BaseModel):
    token: str


class TokenDeleteResult(BaseModel):
    result: bool
    reason: str = "no reason"
