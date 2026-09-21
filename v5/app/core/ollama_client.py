from functools import lru_cache
import ollama
from app.core.config import get_settings

settings = get_settings()


@lru_cache
def get_ollama_client() -> ollama.Client:
    return ollama.Client(host=settings.ollama_url)
