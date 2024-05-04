from jose import jwt
from jose.exceptions import JWTError

from auth.domain.jwt_service import JWTService
from shared.dtos import TokenDto, TokenPayload
from shared.errors import InvalidCredentialsError


class JWTServiceImpl(JWTService):

    def encode(self, payload: TokenPayload) -> TokenDto:
        token = jwt.encode(
            claims=payload.to_dict(),
            key=self.secret_key,
            algorithm=self.jwt_algorithm,
        )

        return TokenDto(access_token=token)

    def decode(self, token: str) -> TokenPayload:
        try:
            payload = jwt.decode(
                token=token, key=self.secret_key, algorithms=[self.jwt_algorithm]
            )

            return TokenPayload(**payload)
        except JWTError:
            raise InvalidCredentialsError
