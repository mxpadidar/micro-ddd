from fastapi import APIRouter, Depends

from auth_service.bootstrap import bus
from auth_service.entrypoints import request_models as rm
from auth_service.entrypoints.dependencies import get_current_user
from auth_service.service_layer import commands
from shared.protocols import UserProtocol

router = APIRouter(prefix="/users", tags=["User"])


@router.post("/register")
async def register_user(data: rm.UserRegisterRequest):
    command = commands.UserRegisterCommand(email=data.email, password=data.password)
    return bus.handle(command)


@router.post("/login")
async def login_user(data: rm.UserLoginRequest):
    command = commands.UserAuthenticateCommand(email=data.email, password=data.password)
    return bus.handle(command)


@router.get("/me")
def user_profile(user: UserProtocol = Depends(get_current_user)):
    return user.serialize()
