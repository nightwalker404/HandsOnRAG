# Document Q&A (RAG) Service — v5

A FastAPI service that lets you upload PDF documents and ask questions about them. It uses **Ollama** for embeddings and chat, and **ChromaDB** as the vector store.

## How it works

1. **Upload** a PDF → it's saved to disk, text is extracted, split into chunks, embedded (via Ollama), and stored in ChromaDB.
2. **Ask a question** → the question is embedded, the most similar chunks are retrieved from ChromaDB, and both are sent to the LLM (via Ollama) to generate a grounded answer.

## Requirements

- Python 3.11+
- [Ollama](https://ollama.com) running locally or reachable over the network
- ChromaDB running as a server (`chroma run`) or in Docker

## Setup

```bash
pip install fastapi uvicorn pydantic-settings ollama chromadb pypdf
```

### `.env` (place in `main/.env`)

```env
APP_HOST=0.0.0.0
APP_PORT=8080

LLM_MODEL=llama3
OLLAMA_URL=http://localhost:11434

EMBEDDING_MODEL=nomic-embed-text

CHROMA_HOST=localhost
CHROMA_PORT=8000
```

Pull the models in Ollama before starting:

```bash
ollama pull llama3
ollama pull nomic-embed-text
```

## Run

```bash
cd main/v5
python -m app.main
```

The API will be available at `http://localhost:8080`.

## Endpoints

### `POST /api/documents/pdf`
Upload a PDF for ingestion.

```bash
curl -X POST http://localhost:8080/api/documents/pdf \
  -F "file=@handbook.pdf"
```

**Response**
```json
{
  "stored_chunk_ids": ["..."],
  "file_path": "main/data/docs/....pdf"
}
```

### `POST /api/chat`
Ask a question grounded in the uploaded documents.

```bash
curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "Where is the server room?", "top_k": 5}'
```

**Response**
```json
{
  "answer": "...",
  "sources": [{"source": "handbook.pdf", "chunk_index": 0, "stored_path": "..."}]
}
```

## Notes

- Vector similarity uses **cosine distance**, the standard choice for text embeddings.
- Uploaded files are renamed to a UUID on disk to avoid filename collisions; the original filename is kept in the chunk metadata (`source`).
- This version handles **PDF only**. Other formats would need their own extractor under `services/extraction/`.
- Single-turn chat only — no conversation history is kept between requests.

## Known limitations / next steps

- No streaming responses (answers return all at once).
- No conversation memory across turns.
- No handling for "no relevant context found" — the LLM is still called even if retrieval returns nothing useful.
