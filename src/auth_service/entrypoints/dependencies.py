from fastapi import Depends, Request
from fastapi.security import HTTPBearer

from auth_service.adapters.auth_service_impl import AuthServiceImpl
from auth_service.adapters.unit_of_work_impl import UnitOfWorkImpl
from auth_service.domain.unit_of_work import UnitOfWork
from shared.auth_service import AuthService
from shared.errors import InvalidCredentialsError
from shared.protocols import UserProtocol
from shared.settings import JWT_ALGORITHM, SECRET_KEY

security = HTTPBearer()


def get_uow() -> UnitOfWork:
    return UnitOfWorkImpl()


def get_auth_service() -> AuthService:
    return AuthServiceImpl(uow=UnitOfWorkImpl())


def get_current_user(
    request: Request, auth_service: AuthServiceImpl = Depends(get_auth_service)
) -> UserProtocol:

    if (auth_header := request.headers.get("Authorization")) is None:
        raise InvalidCredentialsError

    token = auth_header.replace("Bearer ", "")

    token_data = auth_service._decode_jwt(
        token=token,
        secret_key=SECRET_KEY,
        jwt_algorithm=JWT_ALGORITHM,
    )
    return auth_service.get_user_by_id(token_data.user_id)
