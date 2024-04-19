from abc import ABC, abstractmethod

from auth_service.domain.models.user import User


class UserRepo(ABC):

    @abstractmethod
    def add(self, user: User) -> None: ...

    @abstractmethod
    def get(self, id: int) -> User: ...

    @abstractmethod
    def get_by_email(self, email: str) -> User: ...
