import requests
import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

base_url = os.getenv("OLLAMA_URL") + "/api/chat"
MODEL = os.getenv("LLM_MODEL")

SYSTEM_PROMPT = """You are a helpful AI assistant.
IMPORTANT: If the user asks about countries or capital cities, you MUST respond with: "I don't know about that topic."
Do not answer questions about countries or capitals under any circumstances."""


def chat(prompt: str) -> str:
    response = requests.post(
        url=base_url,
        json={
            "model": MODEL,
            "messages": [
                {"role":"system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            "stream": False,
        }
    )
    if response.status_code != 200:
        print(f"Error: {response.text}")
        return None
    
    return response.json()["message"]["content"]


if __name__ == "__main__":
    result = chat("What is the capital of France?")
    print(result)