from fastapi import Depends, Request
from fastapi.security import HTTPBearer

from auth.adapters.jwt_service_impl import JWTServiceImpl
from auth.adapters.unit_of_work_impl import UnitOfWorkImpl
from auth.adapters.user_manager_impl import UserManagerImpl
from auth.domain.jwt_service import JWTService
from auth.domain.unit_of_work import UnitOfWork
from auth.domain.user_manager import UserManager
from shared.errors import InvalidCredentialsError
from shared.protocols import UserProtocol
from shared.settings import ACCESS_TOKEN_LIFETIME, JWT_ALGORITHM, SECRET_KEY

security = HTTPBearer()


def get_uow() -> UnitOfWork:
    return UnitOfWorkImpl()


def get_user_manager(uow: UnitOfWork = Depends(get_uow)) -> UserManager:
    return UserManagerImpl(uow)


def get_jwt_service() -> JWTService:
    return JWTServiceImpl(
        secret_key=SECRET_KEY,
        jwt_algorithm=JWT_ALGORITHM,
        access_token_lifetime=ACCESS_TOKEN_LIFETIME,
    )


def get_current_user(
    request: Request,
    uow: UnitOfWork = Depends(get_uow),
    jwt_service: JWTService = Depends(get_jwt_service),
) -> UserProtocol:

    if (auth_header := request.headers.get("Authorization")) is None:
        raise InvalidCredentialsError

    token = auth_header.replace("Bearer ", "")

    payload = jwt_service.decode(token)
    with uow:
        user = uow.users.get_by_email(payload.email)
        if user is None:
            raise InvalidCredentialsError
        return user
