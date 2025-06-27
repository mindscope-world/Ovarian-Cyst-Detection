# File: api/chatbot.py

from fastapi import APIRouter, HTTPException
# Note: Ensure your filename is 'schemas.py' (plural)
from models.schema import ChatRequest, ChatResponse
from services.chatbot_service import chatbot_service

router = APIRouter()

# Define the list of sample questions so we can return it in the response
SAMPLE_QUESTIONS = [
    "How many patients are from the Nairobi region?",
    "What is the average age of post-menopausal patients?",
    "What is the recommended management for patient OC-1020?",
    "List all patients with a cyst size greater than 9.5 cm.",
    "Which patient has the highest CA 125 level, and what is the value?",
    "What are the most common symptoms reported by pre-menopausal patients?",
]

@router.post(
    "/chatbot",
    response_model=ChatResponse,
    summary="Chat with the Ovarian Cyst Dataset",
    description="""
    > Chat with the ovarian cyst dataset using natural language.

    Ask questions in natural language about the patient dataset.
    
    **Sample Questions:**
        * How many patients are from the Nairobi region?,
        * What is the average age of post-menopausal patients?,
        * What is the recommended management for patient OC-1020?,
        * List all patients with a cyst size greater than 9.5 cm.,
        * Which patient has the highest CA 125 level, and what is the value?,
        * What are the most common symptoms reported by pre-menopausal patients?,
    """

)
async def ask_chatbot(request: ChatRequest):
    """
    This endpoint allows you to query the ovarian cyst dataset using natural language.
    """
    if not chatbot_service.is_configured:
        error_detail = chatbot_service.get_error_details()
        raise HTTPException(status_code=503, detail=error_detail)

    try:
        answer = chatbot_service.get_answer(request.question)
        
        # --- THE FIX IS HERE ---
        # We now provide BOTH 'answer' and 'sample_questions' to the ChatResponse model.
        return ChatResponse(answer=answer, sample_questions=SAMPLE_QUESTIONS)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))