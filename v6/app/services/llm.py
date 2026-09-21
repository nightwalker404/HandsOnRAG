from app.core import get_logger, get_ollama_client, get_settings
from typing import List

logger = get_logger(name=__name__)

settings = get_settings()

class LLMService:
    def __init__(self) -> None:
        self.client = get_ollama_client()
        self.model = settings.LLM_MODEL
        self.embed_model = settings.EMBEDDING_MODEL

    async def embed(self, text: str) -> List[float]:
        """ Convert text into a list of numbers (embedding) """
        response = self.client.embeddings(
            model=self.embed_model,
            prompt=text
        )
        return response["embedding"]

    async def generate(self, prompt: str, temperature: float = 0.3) -> str:
        """ Simple text generation for when we need one time check """
        response = self.client.generate(
            model=self.model,
            prompt=prompt,
            options={"temperature": temperature}
        )
        return response["response"]

    async def chat(self, system: str, user: str, temperature: float = 0.3) -> str:
        """ Chat ponit we use in general """
        response = self.client.chat(
            model=self.model,
            messages=[
                {"role":"system", "content": system},
                {"role":"user", "content": user}
            ],
            options={"temperature": temperature}
        )

        return response["message"]["content"]
