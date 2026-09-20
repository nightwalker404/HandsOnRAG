# v1 - Simple Chat 🤖

Basic prompt → response chat with Ollama.

## Setup

1. Ollama running: `ollama serve`
2. Model pulled: `ollama pull qwen2.5-coder:7b`
3. Install: `pip install requests python-dotenv`
4. Check `.env` has `OLLAMA_URL` and `LLM_MODEL`

## Run

```bash
python3 v1/chat.py
```

## Features

- System prompt to guide behavior
- Topic blocking (keyword filtering)
- Error handling

## Customize

**System prompt:** Edit `SYSTEM_PROMPT` in `chat.py`  
**Blocked topics:** Edit `BLOCKED_TOPICS` list  
**Model:** Change `LLM_MODEL` in `.env`

## What's Next?

Phase 2: Load documents and search them.