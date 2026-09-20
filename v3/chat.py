import ollama
import chromadb
import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

LLM_URL = os.getenv("OLLAMA_URL")
MODEL = os.getenv("LLM_MODEL")
chroma_host = os.getenv("CHROMA_HOST")
chroma_port = int(os.getenv("CHROMA_PORT"))

SYSTEM_PROMPT = """You are a helpful assistant. Answer only based on the provided context. If the answer is not in the context, say you don't know."""

def load_docs(folder_path: str) -> list:
    """Load all .txt files from folder."""
    docs = []
    try:
        for file in Path(folder_path).glob("*.txt"):
            with open(file, 'r') as f:
                content = f.read()
                docs.append({
                    "filename": file.name,
                    "content": content
                })
        print(f"Loaded {len(docs)} documents")
        return docs
    except FileNotFoundError:
        print(f"Error: Folder {folder_path} not found")
        return []

def chunk_text(text: str, chunk_size: int = 300) -> list:
    """Split text into chunks."""
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def put_in_db(docs: list, collection: chromadb.Collection) -> None:
    """Add documents and chunks to ChromaDB."""
    doc_id = 0
    for doc in docs:
        chunks = chunk_text(doc["content"])
        for chunk in chunks:
            collection.add(
                ids=[f"{doc['filename']}-{doc_id}"],
                documents=[chunk],
                metadatas=[{"source": doc["filename"]}]
            )
            doc_id += 1

def chat(user_query: str, context: str) -> str:
    """Send query with context to Ollama."""
    ollama_client = ollama.Client(host=LLM_URL)
    response = ollama_client.chat(
        model=MODEL,
        messages=[
            {'role': 'system', 'content': SYSTEM_PROMPT},
            {'role': 'user', 'content': f"Context: {context}\n\nQuestion: {user_query}"}
        ]
    )
    return response['message']['content']

if __name__ == "__main__":
    chroma_client = chromadb.HttpClient(host=chroma_host, port=chroma_port)
    collection = chroma_client.get_or_create_collection(name="my-collection")

    docs = load_docs("data/docs")

    if docs:
        put_in_db(docs, collection)
        print("Documents stored in ChromaDB\n")
    
    # user_query = "What is the capital of France?"
    user_query = "What is python and how hard is to learn?"
    results = collection.query(
        query_texts=[user_query],
        n_results=3
    )

    if results['documents']:
        context = " ".join(results['documents'][0])
        answer = chat(user_query, context)

        print(f"AI: {answer}")
    else:
        print("No results found")