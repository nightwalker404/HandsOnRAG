from fastapi import FastAPI
from contextlib import asynccontextmanager

from v5.app.db.chroma import settings
from .core import get_settings, get_logger, setup_logging

logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        setup_logging()
        logger.info("Application starting up")

        yield

        logger.info("Application shutting down")
    except Exception as e:
        logger.error(f"we can not countinue for there because of the error:\n {e}")

app = FastAPI(lifespan=lifespan)

if __name__ == "__main__":
    import uvicorn

    settings = get_settings()
    uvicorn.run(app=app, host=settings.app_host, port=settings.app_port)
