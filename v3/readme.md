# v3 - Multiple Documents with ChromaDB 📁

Load multiple documents and chat about them using vector database for semantic search.

## Setup

1. Install ChromaDB: `pip install chromadb`
2. Create docs folder: `mkdir -p data/docs/`
3. Add `.txt` files to `data/docs/` (france.txt, germany.txt, etc.)
4. Check `.env` has `OLLAMA_URL`, `LLM_MODEL`, `CHROMA_HOST`, `CHROMA_PORT`

## Run

```bash
python3 v3/chat.py
```

## How It Works

1. **Load all docs** - Scan `data/docs/` folder
2. **Chunk** - Split each document into 300-char pieces
3. **Store** - Add chunks to ChromaDB (semantic search ready)
4. **Query** - Find best matching chunks using similarity
5. **Answer** - Pass chunks + question to Ollama

## Features

- Multiple documents (folder-based)
- Vector database (ChromaDB)
- Semantic search (not just keywords)
- Metadata tracking (remember source file)

## Customize

**Chunk size:** Edit `chunk_text(text, chunk_size=300)`  
**Number of results:** Edit `collection.query(n_results=3)`  
**Question:** Change in `__main__`

## Example

```bash
$ python3 v3/chat.py
Loaded 3 documents
Documents stored in ChromaDB
Retrieved Context: The capital of France is Paris...
AI: Paris is the capital of France.
```

## What's Next?

Phase 4: Add embeddings and reranking for better accuracy.