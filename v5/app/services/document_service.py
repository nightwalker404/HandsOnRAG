from .chunking import chunk_text
from app.db import upsert_documents

def ingest_document(text: str, source: str) -> list[str]:
    """Chunk a document and store it in the vectorstore."""
    chunks = chunk_text(text=text)
    metadatas = [{"source":source, "chunk_index": i} for i in range(len(chunks))]

    return upsert_documents(texts=chunks, metadatas=metadatas)
