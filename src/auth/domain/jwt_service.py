from abc import ABC, abstractmethod
from datetime import timedelta

from shared.dtos import TokenDto, TokenPayload


class JWTService(ABC):

    def __init__(
        self, secret_key: str, jwt_algorithm: str, access_token_lifetime: timedelta
    ) -> None:
        self.secret_key = secret_key
        self.jwt_algorithm = jwt_algorithm
        self.access_token_lifetime = access_token_lifetime

    @abstractmethod
    def encode(self, payload: TokenPayload) -> TokenDto: ...

    @abstractmethod
    def decode(self, token: str) -> TokenPayload: ...
