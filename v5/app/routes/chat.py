from app.services.chat_service import answer_question
from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException

router = APIRouter()

class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1)
    top_k: int = Field(default=5, gt=1, le=20)


class ChatResponse(BaseModel):
    answer: str
    sources: list[dict]

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        return answer_question(question=request.question, top_k=request.top_k)
    except Exception as e:
            raise HTTPException(status_code=500, detail=f"Chat failed: {e}") from e
