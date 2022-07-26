from pydantic import BaseModel


class UserResponse(BaseModel):
    """
    Response for user name
    """
    name: str
