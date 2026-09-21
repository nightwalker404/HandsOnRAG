from fastapi import APIRouter
from app.routes.chat import router as chat_router
from app.routes.documents import router as documents_router

router = APIRouter(prefix="/api")

router.include_router(chat_router)
router.include_router(documents_router)
