from .chunking import chunk_text
from app.db import upsert_documents
from app.services.extraction import extract_text_from_pdf

def ingest_document(file_bytes: bytes, source: str) -> list[str]:
    """Chunk a document and store it in the vectorstore."""
    text = extract_text_from_pdf(file_bytes=file_bytes)
    chunks = chunk_text(text=text)
    metadatas = [{"source":source, "chunk_index": i} for i in range(len(chunks))]

    return upsert_documents(texts=chunks, metadatas=metadatas)
