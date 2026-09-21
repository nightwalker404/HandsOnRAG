from chromadb import Documents, EmbeddingFunction, Embeddings
from .configs import get_settings
from .ollama_client import get_ollama_client

settings = get_settings()

class OllamaEmbeddingFunction(EmbeddingFunction):
    def __init__(self, model: str = None) -> None:
        self.model = model or settings.embedding_model
        self.client = get_ollama_client()

    def __call__(self, input: Documents) -> Embeddings:
        embeddings = []
        for text in input:
            response = self.client.embeddings(
                model=self.model,
                prompt=text
            )
            embeddings.append(response["embedding"])
        return embeddings
