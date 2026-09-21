from chromadb import Documents, EmbeddingFunction, Embeddings
from .configs import get_settings
import ollama

settings = get_settings()

class OllamaEmbeddingFunction(EmbeddingFunction):
    def __init__(self, model: str = None, base_url: str = None) -> None:
        self.model = model or settings.embedding_model
        self.base_url = base_url or settings.ollama_url
        self.client = ollama.Client(host=self.base_url)

    def __call__(self, input: Documents) -> Embeddings:
        embeddings = []
        for text in input:
            response = self.client.embeddings(
                model=self.model,
                prompt=text
            )
            embeddings.append(response["embedding"])
        return embeddings
