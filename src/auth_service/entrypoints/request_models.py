from pydantic import BaseModel


class UserRegisterRequest(BaseModel):
    email: str
    password: str


class UserLoginRequest(BaseModel):
    email: str
    password: str


class UserAvatarRequest(BaseModel):
    file_id: int
