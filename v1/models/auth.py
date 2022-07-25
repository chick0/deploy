from pydantic import BaseModel


class TokenVerify(BaseModel):
    """
    Response for token verify
    """
    result: bool


class LoginRequest(BaseModel):
    """
    Payload for login
    """
    email: str
    password: str


class LoginResponse(BaseModel):
    """
    Response of login (with auth token)
    """
    token: str
