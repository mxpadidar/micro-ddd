from httpx import AsyncClient

from shared.dtos import UserDto
from shared.errors import InvalidCredentialsError
from shared.logger import Logger
from shared.settings import AUTH_SERVICE_URL

logger = Logger("Authenticate Service")


class AuthService:

    def __init__(self, base_url: str = AUTH_SERVICE_URL) -> None:
        self.client = AsyncClient(base_url=base_url)

    async def verify_token(self, token: str) -> UserDto:
        try:
            response = await self.client.post(
                "/token/verify",
                json={"token": token},
            )

            response.raise_for_status()

            return UserDto.from_dict(response.json())

        except Exception as e:
            logger.exception(f"Error verifying token: {str(e)}")
            raise InvalidCredentialsError
