from fastapi import APIRouter, Depends

from auth.bootstrap import bus
from auth.entrypoints import request_models as rm
from auth.entrypoints.dependencies import get_current_user
from auth.service_layer import commands
from shared.protocols import UserProtocol

router = APIRouter(prefix="/users", tags=["User"])


@router.post("/register")
async def register_user(data: rm.UserRegisterRequest):
    command = commands.UserRegisterCommand(email=data.email, password=data.password)
    return bus.handle(command)


@router.post("/token/verify")
async def verify_token(data: rm.UserVerifyTokenRequest):
    command = commands.VerifyTokenCommand(token=data.token)
    return bus.handle(command)


@router.post("/login")
async def login_user(data: rm.UserLoginRequest):
    command = commands.UserAuthenticateCommand(email=data.email, password=data.password)
    return bus.handle(command)


@router.put("/avatar")
async def add_user_avatar(
    data: rm.UserAvatarRequest, user: UserProtocol = Depends(get_current_user)
):
    command = commands.UserAddAvatarCommand(user_id=user.id, file_id=data.file_id)
    return await bus.handle(command)


@router.get("/me")
def user_profile(user: UserProtocol = Depends(get_current_user)):
    return user.serialize()
