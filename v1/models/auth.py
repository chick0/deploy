from pydantic import BaseModel


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
