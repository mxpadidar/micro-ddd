from pydantic import BaseModel


class UserRegisterRequest(BaseModel):
    email: str
    password: str
    avatar_file_id: int | None


class UserLoginRequest(BaseModel):
    email: str
    password: str


class UserAvatarRequest(BaseModel):
    file_id: int


class UserVerifyTokenRequest(BaseModel):
    token: str
