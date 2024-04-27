import json

from httpx import AsyncClient, HTTPError

from shared.errors import NotFoundError
from shared.logger import Logger

logger = Logger("S3 Client Implementation")


class StorageService:
    def __init__(self, base_url: str):
        self.client = AsyncClient(base_url=base_url)

    async def get_file_by_id(self, file_id: int) -> str:
        try:
            response = await self.client.get(f"/{file_id}")
            response.raise_for_status()
            url = response.text
            return json.loads(url)
        except HTTPError as e:
            logger.exception(f"Error getting file: {str(e)}")
            raise NotFoundError("File not found")
