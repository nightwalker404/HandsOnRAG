import ollama
import chromadb
import os
from pathlib import Path
from dotenv import load_dotenv
from process_pdf import embedding
from db import search_in_db

env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

LLM_URL = os.getenv("OLLAMA_URL")
MODEL = os.getenv("LLM_MODEL")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
RERANK_MODEL = os.getenv("RERANK_MODEL")

chroma_host = os.getenv("CHROMA_HOST")
chroma_port = int(os.getenv("CHROMA_PORT"))

SYSTEM_PROMPT = """You are a helpful assistant. Answer only based on the provided context. If the answer is not in the context, say you don't know."""

def chat(prompt: str, ollama_client: ollama.Client, collection: chromadb.Collection):
    search_results = search_in_db(ollama_client=ollama_client, query=prompt, model=EMBEDDING_MODEL, collection=collection)

    response = ollama_client.chat(
        model=MODEL,
        messages=[
            {"role":"system", "content":SYSTEM_PROMPT + f"content: {search_results}"},
            {"role":"user", "content":prompt}
        ],
        stream=False
    )
    return response['message']['content']

if __name__ == "__main__":
    ollama_client = ollama.Client(LLM_URL)
    chroma_client = chromadb.HttpClient(host=chroma_host, port=chroma_port)
    collection = chroma_client.get_or_create_collection(name="v4-collection")

    query = """
    What is the main topic of this PDF? 
    And is the system called PIER-QA?
    """

    embedding(embed_model=EMBEDDING_MODEL, ollama_client=ollama_client, collection=collection)
    
    answer = chat(prompt = query, ollama_client=ollama_client, collection=collection)
    print(f"AI: {answer}")