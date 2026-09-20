from pypdf import PdfReader
import ollama
import chromadb

def extract_text_from_pdf(pdf_path: str) -> str:
    """ Extract all text from a PDF """
    pdf = PdfReader(pdf_path)
    text = ""

    for page in pdf:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n\n"
    return text.strip()
        

def split_text(text: str, chunk_size: int = 800, overlap: int = 100) -> list[str]:
    """ text splitter """
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]

        if end < text_length:
            last_period = chunk.rfind(". ")
            last_newline = chunk.rfind("\n")

            cut_point = max(last_period, last_newline)

            if cut_point > chunk_size // 2:
                end = start + cut_point + 1
                chunk = text[start:end]

        chunks.append(chunk.strip())
        start = end - overlap

    return [c for c in chunks if c]

def embed_chunks(chunks: list[str], ollama_client: ollama.Client, model: str) -> list[list[float]]:
    """ Embed chunks using nomic-embed-text via Ollama """
    embeddings = []
    for i, chunk in enumerate(chunks):
        response = ollama_client.embed(
            model=model,
            input=f"search_document: {chunk}"
        )
        embeddings.append(response["embeddings"][0])
    return embeddings

def save_to_chromadb(chunks: list[str], embeddings: list[list[float]], collection: chromadb.Collection, file_name: str):
    """Add documents and chunks to ChromaDB."""
    for i, chunk in enumerate(chunks):
        collection.add(
            ids=f"chunk_{i}",
            documents=chunk,
            embeddings=embeddings[i],
            metadatas=[{"source": file_name}]
        )   


def embedding(embed_model: str, ollama_client: ollama.Client, collection: chromadb.Collection):
    """ the main embedding part to run """
    file_name = "data/docs/test.pdf"
    text = extract_text_from_pdf(file_name)
    chunks = split_text(text=text)
    embeddings = embed_chunks(chunks=chunks, ollama_client=ollama_client, model=embed_model)
    save_to_chromadb(chunks=chunks, embeddings=embeddings, collection=collection, file_name=file_name)


