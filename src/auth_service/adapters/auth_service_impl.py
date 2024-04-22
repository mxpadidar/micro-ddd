from datetime import datetime

from jose import jwt
from passlib.context import CryptContext

from auth_service.domain.models.user import User
from auth_service.domain.unit_of_work import UnitOfWork
from shared.auth_service import AuthService
from shared.dtos import TokenPayload
from shared.errors import InvalidCredentialsError
from shared.protocols import UserProtocol
from shared.settings import ACCESS_TOKEN_LIFETIME, JWT_ALGORITHM, SECRET_KEY


class AuthServiceImpl(AuthService):

    def __init__(self, uow: UnitOfWork) -> None:
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.uow = uow

    def get_user_by_id(self, id: int) -> UserProtocol:
        with self.uow:
            return self.uow.users.get(id)

    def register_user(self, email: str, password: str) -> UserProtocol:
        with self.uow:
            user = User(email=email, hashed_password=self._hash_password(password))
            self.uow.users.add(user)
            self.uow.commit()
            return user

    def authenticate_user(self, email: str, password: str) -> User:
        with self.uow:
            user = self.uow.users.get_by_email(email)

            if self._verify_password(password, user.hashed_password):
                return user

            raise InvalidCredentialsError

    def generate_token(self, user: User) -> str:
        return self._generate_jwt(
            user_id=user.id,
            expires_at=datetime.now() + ACCESS_TOKEN_LIFETIME,
            secret_key=SECRET_KEY,
            jwt_algorithm=JWT_ALGORITHM,
        )

    def _hash_password(self, plain_password: str) -> str:
        return self.pwd_context.hash(plain_password)

    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def _generate_jwt(
        self, user_id: int, expires_at: datetime, secret_key: str, jwt_algorithm: str
    ) -> str:
        return jwt.encode(
            claims={"user_id": user_id, "expires_at": expires_at.isoformat()},
            key=secret_key,
            algorithm=jwt_algorithm,
        )

    def _decode_jwt(
        self, token: str, secret_key: str, jwt_algorithm: str
    ) -> TokenPayload:

        print("token    ", token)

        try:
            payload = jwt.decode(
                token=token, key=secret_key, algorithms=[jwt_algorithm]
            )

            print(payload)
            return TokenPayload(**payload)
        except Exception:
            raise Exception("Invalid token")
