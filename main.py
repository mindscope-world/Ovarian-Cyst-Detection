import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import joblib
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

# Import the routers from the api module
from api import prediction, chatbot

app = FastAPI(
    title="Ovarian Cyst Analysis API",
    description="An API for predicting ovarian cyst management and chatting with patient data using Gemini.",
    version="2.0.0"
)

# ✅ Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",             # React dev server (local)
        "https://afya-sasa.vercel.app",      # Deployed frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Optional: Serve favicon to avoid 404 error
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("static/favicon.ico")  # Ensure this file exists

# --- Startup Event ---
@app.on_event("startup")
async def startup_event():
    """
    Loads all necessary artifacts for the application. The chatbot service is
    initialized automatically when its module is first imported.
    """
    MODEL_ARTIFACTS_PATH = 'ovarian_cyst_inference_artifacts.joblib'
    try:
        artifacts = joblib.load(MODEL_ARTIFACTS_PATH)
        
        # Populate the variables in the 'prediction' module
        prediction.model = artifacts['model']
        prediction.mlb_encoder = artifacts['mlb_encoder']
        prediction.symptom_column_names = artifacts['symptom_column_names']
        prediction.ultrasound_one_hot_columns = artifacts['ultrasound_one_hot_columns']
        prediction.pipeline_input_columns = artifacts['pipeline_input_columns']
        
        print(f"Prediction model and artifacts loaded successfully from {MODEL_ARTIFACTS_PATH}.")

    except FileNotFoundError:
        print(f"FATAL ERROR: Prediction model file not found at {MODEL_ARTIFACTS_PATH}")
    except Exception as e:
        print(f"FATAL ERROR: Failed to load prediction model artifacts: {e}")

# --- Include Routers ---
app.include_router(prediction.router, tags=["1. ML Prediction"])
app.include_router(chatbot.router, tags=["2. AI Chatbot"])

# --- Root Endpoint ---
@app.get("/", summary="API Welcome", tags=["Root"])
async def read_root():
    return {
        "message": "Welcome to the Ovarian Cyst Analysis API",
        "documentation": "/docs",
        "endpoints": {
            "/predict": "POST patient data to get a management recommendation.",
            "/chatbot": "POST a question to chat with the patient dataset."
        }
    }

# --- Main execution block ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
