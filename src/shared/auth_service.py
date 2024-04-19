from abc import ABC, abstractmethod

from shared.protocols import UserProtocol


class AuthService(ABC):

    @abstractmethod
    def get_user_by_id(self, id: int) -> UserProtocol: ...

    @abstractmethod
    def register_user(self, email: str, password: str) -> UserProtocol: ...

    @abstractmethod
    def authenticate_user(self, email: str, password: str) -> UserProtocol: ...

    @abstractmethod
    def generate_token(self, user: UserProtocol) -> str: ...
