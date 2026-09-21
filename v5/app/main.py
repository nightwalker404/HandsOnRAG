from fastapi import FastAPI
from contextlib import asynccontextmanager
from .core import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application is starting up")
    yield
    print("Application is shutting down")


app = FastAPI(lifespan=lifespan)


if __name__ == "__main__":
    import uvicorn

    settings = get_settings()
    uvicorn.run(
        app=app,
        host=settings.app_host,
        port=settings.app_port,
    )
