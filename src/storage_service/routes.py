import httpx
from fastapi import APIRouter

from shared.settings import AUTH_SERVICE_URL

router = APIRouter(prefix="/storage", tags=["Storage"])


@router.get("/user/{user_id}")
async def get_user_from_auth_service(user_id: int):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{AUTH_SERVICE_URL}/auth/user/{user_id}")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            # Handle error
            return {"error": str(e)}
