from fastapi import APIRouter, UploadFile
from app.services.document_service import ingest_document

router = APIRouter()

@router.post("/documents")
async def upload_document(file: UploadFile):
    file_bytes = await file.read()
    ids = ingest_document(file_bytes, source=file.filename)
    return {"stored_chunk_ids": ids}
