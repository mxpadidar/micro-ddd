from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from product.bootstrap import auth_service
from shared.errors import InvalidCredentialsError
from shared.protocols import UserProtocol

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def current_user(token: str = Depends(oauth2_scheme)) -> UserProtocol:
    try:
        response = auth_service.verify_token(token)
        return await response
    except InvalidCredentialsError:
        raise InvalidCredentialsError
