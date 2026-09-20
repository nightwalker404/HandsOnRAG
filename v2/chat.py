import requests
import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

base_url = os.getenv("OLLAMA_URL") + "/api/chat"
MODEL = os.getenv("LLM_MODEL")

SYSTEM_PROMPT = """You are a helpful assistant. Answer only based on the provided context. If the answer is not in the context, say you don't know."""

def load_doc(file_path: str) -> str:
    """Load a document from disk."""
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File {file_path} not found")
        return ""

def chunk_text(text: str, chunk_size: int = 300) -> list:
    """Split text into chunks of size chunk_size."""
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    return chunks


def search_chunks(chunks: list, question: str) -> str:
    """Find the best matching chunk."""
    question_words: list = question.lower().split()
    best_chunk = ""
    best_score = 0

    for chunk in chunks:
        chunk_lower = chunk.lower()
        score = sum(1 for word in question_words if word in chunk_lower)
        if score > best_score:
            best_score = score
            best_chunk = chunk
    
    return best_chunk

def chat(content: str, question: str) -> str:
    response = requests.post(
        url=base_url,
        json={
            "model": MODEL,
            "messages":[
                {"role":"system", "content":SYSTEM_PROMPT},
                {"role":"user", "content":f"Content:{content}\n\nQuestion:{question}"}
            ],
            "stream": False
        }
    )
    if response.status_code == 200:
        result = response.json()
        answer = result["message"]["content"]
        return answer
    else:
        print("Error:", response.status_code, response.text)
        return None

if __name__ == "__main__":
    doc_content: str = load_doc("data/docs/france.txt")

    question = "What is the capital of France?"

    chunks = chunk_text(text=doc_content)

    relevant_chunk = search_chunks(chunks, question)

    result = chat(content=relevant_chunk, question=question)
    print(result)

