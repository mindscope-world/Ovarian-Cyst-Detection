# File: api/prediction.py

import pandas as pd
from fastapi import APIRouter, HTTPException
from models.schema import OvarianCystData, PredictionResponse

# These global variables will be populated by the main app's startup event
# to avoid loading the model multiple times.
model = None
mlb_encoder = None
symptom_column_names = None
ultrasound_one_hot_columns = None
pipeline_input_columns = None

router = APIRouter()

def preprocess_input(data: OvarianCystData) -> pd.DataFrame:
    """
    Applies the same preprocessing steps to a single input record as done during training.
    """
    raw_input_df = pd.DataFrame([{
        'Age': data.Age,
        'Menopause Status': data.Menopause_Status,
        'Cyst Size cm': data.Cyst_Size_cm,
        'Cyst Growth Rate cm/month': data.Cyst_Growth_Rate_cm_month,
        'CA 125 Level': data.CA_125_Level,
        'Ultrasound Features': data.Ultrasound_Features,
        'Reported Symptoms': data.Reported_Symptoms
    }])

    menopause_mapping = {'Pre-menopausal': 0, 'Post-menopausal': 1}
    raw_input_df['Menopause Status'] = raw_input_df['Menopause Status'].map(menopause_mapping)

    raw_input_df['Reported Symptoms'] = raw_input_df['Reported Symptoms'].fillna('')
    symptoms_list_for_input = raw_input_df['Reported Symptoms'].apply(
        lambda x: [s.strip().lower() for s in x.split(',') if s.strip()]
    ).tolist()

    symptoms_encoded_input = mlb_encoder.transform(symptoms_list_for_input)
    symptoms_df_input = pd.DataFrame(symptoms_encoded_input, columns=symptom_column_names, index=raw_input_df.index)
    processed_df = pd.concat([raw_input_df.drop('Reported Symptoms', axis=1), symptoms_df_input], axis=1)

    for us_col in ultrasound_one_hot_columns:
        feature_name = us_col.replace('US_', '')
        processed_df[us_col] = (processed_df['Ultrasound Features'] == feature_name).astype(int)

    processed_df.drop('Ultrasound Features', axis=1, inplace=True)
    
    final_input_df = pd.DataFrame(0, index=processed_df.index, columns=pipeline_input_columns)
    
    cols_to_copy = [col for col in processed_df.columns if col in final_input_df.columns]
    final_input_df[cols_to_copy] = processed_df[cols_to_copy]
    
    final_input_df.columns = final_input_df.columns.astype(str)

    return final_input_df

@router.post(
    "/predict",
    response_model=PredictionResponse,
    summary="Predict Ovarian Cyst Management",
    description="Predicts the recommended management for an ovarian cyst based on patient data."
)
async def predict_management(data: OvarianCystData):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded. Please ensure the application started correctly.")

    try:
        processed_input = preprocess_input(data)
        prediction = model.predict(processed_input)
        predicted_management = prediction[0]
        return PredictionResponse(recommended_management=predicted_management)
    except Exception as e:
        print(f"Prediction Error: {e}")
        raise HTTPException(status_code=400, detail=f"Prediction failed. Check input data. Error: {e}")