from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from shared.dtos import UserDto
from shared.errors import InvalidCredentialsError
from storage.bootstrap import auth_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def current_user(token: str = Depends(oauth2_scheme)) -> UserDto:
    try:
        return await auth_service.verify_token(token)
    except InvalidCredentialsError:
        raise InvalidCredentialsError
