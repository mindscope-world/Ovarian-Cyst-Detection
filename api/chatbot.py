# File: api/chatbot.py

from fastapi import APIRouter, HTTPException # type: ignore
from models.schema import ChatRequest, ChatResponse # type: ignore
from services.chatbot_service import chatbot_service

router = APIRouter() # type: ignore

SAMPLE_QUESTIONS = [
    "How many patients are from the Nairobi region?",
    "What is the average age of post-menopausal patients?",
    "What is the recommended management for patient OC-1020?",
    "List all patients with a cyst size greater than 9.5 cm.",
    "Which patient has the highest CA 125 level, and what is the value?",
    "What are the most common symptoms reported by pre-menopausal patients?",
]

@router.post( # type: ignore
    "/chatbot",
    response_model=ChatResponse,
    summary="Chat with the Ovarian Cyst Dataset",
    description="Ask questions in natural language about the patient dataset. The chatbot uses the Gemini model to analyze the provided CSV data and provide answers."
)
async def ask_chatbot(request: ChatRequest): # type: ignore
    """
    This endpoint allows you to query the ovarian cyst dataset using natural language.

    - **question**: The question you want to ask about the data.

    The chatbot will respond based *only* on the data it was provided.
    """
    try:
        answer = chatbot_service.get_answer(request.question) # type: ignore
        return ChatResponse(answer=answer, sample_questions=SAMPLE_QUESTIONS) # type: ignore
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))