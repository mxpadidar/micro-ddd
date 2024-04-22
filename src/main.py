from fastapi import FastAPI

from auth_service.entrypoints.routes import router as auth_router
from shared.db_setup import db_health_check
from storage_service.entrypoints.routes import router as storage_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(storage_router)


@app.get("/")
async def database_health_check():
    return db_health_check()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)
