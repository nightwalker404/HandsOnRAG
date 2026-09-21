import chromadb
import uuid
from chromadb.config import Settings as ChromaClientSettings
from functools import lru_cache
from app.core import get_settings, OllamaEmbeddingFunction


settings = get_settings()


@lru_cache
def get_chroma_client() -> chromadb.HttpClient:
    return chromadb.HttpClient(
        host=settings.chroma_host,
        port=settings.chroma_port,
        settings=ChromaClientSettings(anonymized_telemetry=False),
    )


@lru_cache
def get_document_collection():
    client = get_chroma_client()
    return client.get_or_create_collection(
        name="documents",
        embedding_function=OllamaEmbeddingFunction(),
        metadata={"hnsw:space": "cosine"},
    )


def upsert_documents(texts: list[str], metadatas: list[dict] | None = None, ids: list[str] | None = None) -> list[str]:
    """Embed and store documents, generating IDs if not provided."""
    metadatas = metadatas or [{} for _ in texts]
    ids = ids or [str(uuid.uuid4()) for _ in texts]

    collection = get_document_collection()
    collection.upsert(ids=ids, metadatas=metadatas, documents=texts)

    return ids


def search_similar_documents(query_text: str, top_k: int = 5) -> dict:
    """Return the top_k most similar documents to query_text."""
    collection = get_document_collection()
    return collection.query(query_texts=[query_text], n_results=top_k)


def delete_documents(ids: list[str]) -> None:
    collection = get_document_collection()
    collection.delete(ids=ids)
