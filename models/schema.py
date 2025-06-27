# models/schemas.py

# File: models/schemas.py

from pydantic import BaseModel # type: ignore
from typing import Optional, List

# --- Prediction Endpoint Models ---

class OvarianCystData(BaseModel): # type: ignore
    """
    Pydantic model for the input data for the /predict endpoint.
    """
    Age: int
    Menopause_Status: str
    Cyst_Size_cm: float
    Cyst_Growth_Rate_cm_month: float
    CA_125_Level: int
    Ultrasound_Features: str
    Reported_Symptoms: Optional[str] = ""

class PredictionResponse(BaseModel): # type: ignore
    """
    Pydantic model for the response from the /predict endpoint.
    """
    recommended_management: str


# --- Chatbot Endpoint Models ---

class ChatRequest(BaseModel): # type: ignore
    """
    Pydantic model for the input to the /chatbot endpoint.
    """
    question: str

class ChatResponse(BaseModel): # type: ignore
    """
    Pydantic model for the response from the /chatbot endpoint.
    Includes the answer and sample questions for user guidance.
    """
    answer: str
    sample_questions: List[str]