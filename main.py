import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import numpy as np

# Initialize FastAPI app
app = FastAPI(
    title="Ovarian Cyst Management Prediction API",
    description="API for predicting recommended management for ovarian cysts based on patient data.",
    version="1.0.0"
)

# Define the path to the saved model and preprocessing artifacts
# Make sure this file (ovarian_cyst_inference_artifacts.joblib) is in the same directory as your FastAPI script
MODEL_ARTIFACTS_PATH = 'ovarian_cyst_inference_artifacts.joblib'

# Global variables to store the loaded model and preprocessing artifacts
model = None
mlb_encoder = None
symptom_column_names = None
ultrasound_one_hot_columns = None
pipeline_input_columns = None # This is the full list of columns expected by the model's pipeline after manual preprocessing
numerical_features = None # Used for debugging, not strictly for pipeline inference

# Load the model and preprocessing artifacts when the application starts
@app.on_event("startup")
async def load_artifacts():
    """
    Loads the trained model and all necessary preprocessing artifacts from the joblib file
    when the FastAPI application starts.
    """
    global model, mlb_encoder, symptom_column_names, ultrasound_one_hot_columns, pipeline_input_columns, numerical_features
    try:
        # Load all artifacts saved during training
        artifacts = joblib.load(MODEL_ARTIFACTS_PATH)
        model = artifacts['model']
        mlb_encoder = artifacts['mlb_encoder']
        symptom_column_names = artifacts['symptom_column_names']
        ultrasound_one_hot_columns = artifacts['ultrasound_one_hot_columns']
        pipeline_input_columns = artifacts['pipeline_input_columns']
        numerical_features = artifacts['numerical_features'] # For reference/validation

        print(f"Model and artifacts loaded successfully from {MODEL_ARTIFACTS_PATH}")
        print(f"Expected pipeline input columns: {pipeline_input_columns}")
        print(f"MLB classes: {mlb_encoder.classes_}")

    except FileNotFoundError:
        print(f"Error: Model artifacts file not found at {MODEL_ARTIFACTS_PATH}")
        raise HTTPException(status_code=500, detail="Model not found. Ensure 'ovarian_cyst_inference_artifacts.joblib' is in the correct directory.")
    except Exception as e:
        print(f"Error loading model artifacts: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to load model artifacts: {e}")

# Define the input data model for the API using Pydantic
class OvarianCystData(BaseModel):
    """
    Pydantic model defining the expected input features for prediction.
    Corresponds to the original feature columns in your dataset.
    """
    Age: int
    Menopause_Status: str # "Pre-menopausal" or "Post-menopausal"
    Cyst_Size_cm: float
    Cyst_Growth_Rate_cm_month: float
    CA_125_Level: int
    Ultrasound_Features: str # e.g., "Septated cyst", "Simple cyst", "Solid mass", etc.
    Reported_Symptoms: Optional[str] = "" # Comma-separated string, e.g., "Pelvic pain, Nausea, Bloating"


# Preprocessing function for a single input record
def preprocess_input(data: OvarianCystData) -> pd.DataFrame:
    """
    Applies the same preprocessing steps to a single input record as done during training.
    Ensures the input DataFrame has the correct columns and order for the model pipeline.
    """
    # Create a DataFrame from the input data, matching original column names from the notebook
    # Note: Pydantic field names use snake_case for Python, but actual column names in pandas might be different.
    # Adjust mapping here if needed.
    raw_input_df = pd.DataFrame([{
        'Age': data.Age,
        'Menopause Status': data.Menopause_Status,
        'Cyst Size cm': data.Cyst_Size_cm,
        'Cyst Growth Rate cm/month': data.Cyst_Growth_Rate_cm_month,
        'CA 125 Level': data.CA_125_Level,
        'Ultrasound Features': data.Ultrasound_Features,
        'Reported Symptoms': data.Reported_Symptoms
    }])

    # --- 1. Handle 'Menopause Status' encoding
    menopause_mapping = {'Pre-menopausal': 0, 'Post-menopausal': 1}
    raw_input_df['Menopause Status'] = raw_input_df['Menopause Status'].map(menopause_mapping)

    # --- 2. Handle 'Reported Symptoms' (MultiLabelBinarizer)
    # Fill NaN with empty string to avoid errors in split
    raw_input_df['Reported Symptoms'] = raw_input_df['Reported Symptoms'].fillna('')
    # Split symptoms, strip whitespace, convert to lowercase, and filter out empty strings
    symptoms_list_for_input = raw_input_df['Reported Symptoms'].apply(
        lambda x: [s.strip().lower() for s in x.split(',') if s.strip()]
    ).tolist() # Convert to list of lists for mlb_encoder.transform

    # Transform symptoms using the *fitted* MultiLabelBinarizer
    # Note: mlb_encoder.transform expects a list of lists
    symptoms_encoded_input = mlb_encoder.transform(symptoms_list_for_input)
    symptoms_df_input = pd.DataFrame(symptoms_encoded_input, columns=symptom_column_names, index=raw_input_df.index)

    # Concatenate symptom features and drop original column
    processed_df = pd.concat([raw_input_df.drop('Reported Symptoms', axis=1), symptoms_df_input], axis=1)

    # --- 3. Handle 'Ultrasound Features' (One-Hot Encoding)
    # Create one-hot columns for the input's Ultrasound_Features.
    # Ensure all possible columns (from training) are present, filling with 0 if not
    for us_col in ultrasound_one_hot_columns:
        feature_name = us_col.replace('US_', '') # Extract original feature name
        # Check if the current input's ultrasound feature matches this column
        # Note: If the input has multiple ultrasound features, this needs adjustment
        # Based on the notebook, it seems 'Ultrasound Features' is a single categorical value.
        processed_df[us_col] = (processed_df['Ultrasound Features'] == feature_name).astype(int)

    # Drop the original 'Ultrasound Features' column
    processed_df.drop('Ultrasound Features', axis=1, inplace=True)

    # --- Ensure column order and presence matches the training data's X.columns
    # Create a new DataFrame with the correct column order and filled with zeros initially
    final_input_df = pd.DataFrame(0, index=processed_df.index, columns=pipeline_input_columns)

    # Fill the new DataFrame with values from the preprocessed input
    # Only copy columns that are actually in final_input_df
    cols_to_copy = [col for col in processed_df.columns if col in final_input_df.columns]
    final_input_df[cols_to_copy] = processed_df[cols_to_copy]

    # Important: Ensure column names are strings before passing to sklearn pipeline
    final_input_df.columns = final_input_df.columns.astype(str)

    return final_input_df

# Define the prediction endpoint
@app.post("/predict")
async def predict_management(data: OvarianCystData):
    """
    Predicts the recommended management for an ovarian cyst based on the provided patient data.
    """
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded. Please ensure the application started correctly.")

    try:
        # Preprocess the incoming data
        processed_input = preprocess_input(data)

        # Make prediction using the loaded model
        prediction = model.predict(processed_input)
        # Assuming the model outputs a single prediction string
        predicted_management = prediction[0]

        return {"recommended_management": predicted_management}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction failed: {e}")


