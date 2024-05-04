from fastapi import FastAPI

from auth.entrypoints.routes import router as auth_router
from product.entrypoints.routes import router as product_router
from storage.entrypoints.routes import router as storage_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(storage_router)
app.include_router(product_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)
