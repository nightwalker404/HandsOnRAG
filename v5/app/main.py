from fastapi import FastAPI
from contextlib import asynccontextmanager
from .core import get_settings
from .routes import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application is starting up")
    yield
    print("Application is shutting down")


app = FastAPI(lifespan=lifespan)
app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn

    settings = get_settings()
    uvicorn.run(
        app=app,
        host=settings.app_host,
        port=settings.app_port,
    )
