from fastapi import APIRouter, UploadFile
from app.services.document_service import ingest_document

router = APIRouter()

@router.post("/documents/pdf")
async def upload_document(file: UploadFile):
    file_bytes = await file.read()
    result = ingest_document(file_bytes=file_bytes, source=file.filename)
    return result
