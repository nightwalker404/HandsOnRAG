from .chunking import chunk_text
from app.db import upsert_documents
from app.services.extraction import extract_text_from_pdf
from .storage import save_uploaded_file

def ingest_document(file_bytes: bytes, source: str) -> dict:
    """Chunk a document and store it in the vectorstore."""
    saved_path = save_uploaded_file(file_bytes, source)
    text = extract_text_from_pdf(file_bytes=file_bytes)
    chunks = chunk_text(text=text)
    metadatas = [{"source":source, "stored_path": str(saved_path), "chunk_index": i} for i in range(len(chunks))]

    ids = upsert_documents(texts=chunks, metadatas=metadatas)
    return {"stored_chunk_ids": ids, "file_path": str(saved_path)}
