from fastapi import APIRouter, Depends

from auth.bootstrap import bus
from auth.domain.entities.user import User
from auth.entrypoints import request_models as rm
from auth.entrypoints.dependencies import get_current_user
from auth.service_layer import messages

router = APIRouter(prefix="/users", tags=["User"])


@router.post("/register")
async def register_user(data: rm.UserRegisterRequest):
    command = messages.UserRegisterCommand(
        email=data.email, password=data.password, avatar_file_id=data.avatar_file_id
    )
    return await bus.handle(command)


@router.post("/token/verify")
async def verify_token(data: rm.UserVerifyTokenRequest):
    command = messages.VerifyTokenCommand(token=data.token)
    return bus.handle(command)


@router.post("/login")
async def login_user(data: rm.UserLoginRequest):
    command = messages.UserAuthenticateCommand(email=data.email, password=data.password)
    return bus.handle(command)


@router.get("/me")
def user_profile(user: User = Depends(get_current_user)):
    return user.serialize()
