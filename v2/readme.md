# v2 - Single Document Chat 📄

Load a document and chat about it. The first real RAG step.

## Setup

1. Ollama running: `ollama serve`
2. Install: `pip install requests python-dotenv`
3. Create document: `data/docs/france.txt` (your content)
4. Check `.env` has `OLLAMA_URL` and `LLM_MODEL`

## Run

```bash
python3 v2/chat.py
```

## How It Works

1. **Load** - Read document from disk
2. **Chunk** - Split into 300-char pieces
3. **Search** - Find chunks matching the question (keyword counting)
4. **Send** - Pass best chunk + question to Ollama
5. **Answer** - Model answers based on your document

## Customize

**Document path:** Change in `__main__`  
**Chunk size:** Edit `chunk_text(text, chunk_size=300)`  
**Question:** Change in `__main__`

## Example

```bash
$ python3 v2/chat.py
The capital of France is Paris.
```

## What's Next?

Phase 3: Load multiple documents from a folder.