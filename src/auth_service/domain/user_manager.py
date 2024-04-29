from abc import ABC, abstractmethod

from auth_service.domain.models.user import User
from auth_service.domain.unit_of_work import UnitOfWork
from shared.errors import InvalidCredentialsError


class UserManager(ABC):

    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    def authenticate_user(self, email: str, password: str) -> User:
        with self.uow:
            user = self.uow.users.get_by_email(email)

            if self.verify_password(password, user.hashed_password):
                return user

            raise InvalidCredentialsError

    def create_user(self, email: str, password: str) -> User:
        with self.uow:
            user = User(email=email, hashed_password=self.hash_password(password))
            self.uow.users.add(user)
            self.uow.commit()
            return user

    def create_superuser(self, email: str, password: str) -> User:
        with self.uow:
            user = User(
                email=email,
                hashed_password=self.hash_password(password),
                is_superuser=True,
            )
            self.uow.users.add(user)
            self.uow.commit()
            return user

    def get_user_by_email(self, email: str) -> User:
        with self.uow:
            return self.uow.users.get_by_email(email)

    @abstractmethod
    def verify_password(self, plain_password: str, hashed_password: str) -> bool: ...

    @abstractmethod
    def hash_password(self, plain_password: str) -> str: ...
