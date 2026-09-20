import chromadb
import ollama

def save_to_chromadb(chunks: list[str], embeddings: list[list[float]], collection: chromadb.Collection, file_name: str):
    """Add documents and chunks to ChromaDB."""
    for i, chunk in enumerate(chunks):
        collection.add(
            ids=f"chunk_{i}",
            documents=chunk,
            embeddings=embeddings[i],
            metadatas=[{"source": file_name}]
        )   

def search_in_db(collection: chromadb.Collection, ollama_client: ollama.Client, model:str, query: str, k: int = 5):
    """Search your PDF collection and return top-k chunks."""
    query_emb = ollama_client.embed(
        model=model,
        input=f"search_document: {query}"
    )["embeddings"][0]

    results = collection.query(
        query_embeddings=[query_emb],
        n_results=k,
        include=["documents", "metadatas"]
    )

    return results