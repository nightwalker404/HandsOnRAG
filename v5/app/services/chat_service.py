from app.core import get_settings, get_ollama_client
from app.db import search_similar_documents
from app.prompts.prompt_loader import load_prompt

def build_context(chunks: list[str]) -> str:
    """ Join retrieved chunks into a single context block for the prompt. """
    return "\n\n---\n\n".join(chunks)


def build_messages(question: str, context: str) -> list[dict]:
    """ Load the prompt template and fill in context + question. """
    template = load_prompt("v1")[0]
    filled_content = template["content"].format(context=context, query=question)
    return [{"role": template["role"], "content": filled_content}]

def answer_question(question: str, top_k: int = 5) -> dict:
    """ Retrieve relevant chunks and generate an answer grounded in them. """
    results = search_similar_documents(question, top_k=top_k)

    chunks = results["documents"][0]
    sources = results["metadatas"][0]

    context = build_context(chunks)
    messages = build_messages(question, context)

    client = get_ollama_client()
    settings = get_settings()

    response = client.chat(model=settings.llm_model, messages=messages)

    return {
        "answer": response["message"]["content"],
        "sources": sources,
    }
