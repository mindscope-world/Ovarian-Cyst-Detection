# Ovarian Cyst Analysis API

This project provides a powerful API for analyzing ovarian cyst data, built with Python and FastAPI. It offers two primary functionalities:
1.  **Machine Learning Prediction:** An endpoint that uses a pre-trained scikit-learn model to predict the recommended management plan for a patient based on their clinical data.
2.  **AI-Powered Chatbot:** An intelligent chatbot, powered by Google's Gemini Pro model, that allows users to ask natural language questions about the entire patient dataset.

The application is built with a modular and scalable structure, making it easy to maintain and extend.

## ✨ Features

- **ML-Powered Predictions**: Get instant recommendations for patient management (`Observation`, `Surgery`, `Medication`, etc.).
- **Conversational AI Chatbot**: Interact with your data using natural language. Ask for statistics, filter data, or look up specific patient information.
- **FastAPI Backend**: A high-performance, easy-to-use asynchronous API framework.
- **Interactive Documentation**: Automatic, interactive API documentation powered by Swagger UI and ReDoc.
- **Modular Project Structure**: Code is organized by feature (`api`, `services`, `core`, `models`) for better maintainability.
- **Environment-based Configuration**: Securely manage API keys and settings using a `.env` file.

## 🛠️ Tech Stack

- **Backend**: FastAPI, Uvicorn
- **Machine Learning**: Scikit-learn, Pandas, Joblib
- **Generative AI**: Google Gemini Pro (`google-generativeai`)
- **Language**: Python 3.10+

## 📁 Project Structure

The project is organized into distinct modules for clear separation of concerns.

```
/
├── .env                  # Environment variables (API keys, settings)
├── main.py               # Main application entrypoint
├── ovarian_cyst_inference_artifacts.joblib # The trained ML model
├── requirements.txt      # Project dependencies
|
├── data/
│   └── Ovarian_Cyst_Track_Data.csv  # The dataset for the chatbot
|
├── api/                  # API endpoint definitions (routers)
│   ├── __init__.py
│   ├── prediction.py
│   └── chatbot.py
|
├── services/             # Business logic (e.g., calling Gemini)
│   ├── __init__.py
│   └── chatbot_service.py
|
├── core/                 # Application configuration
│   ├── __init__.py
│   └── config.py
|
└── models/               # Pydantic data models (schemas)
    ├── __init__.py
    └── schemas.py
```

## 🚀 Getting Started

Follow these instructions to get the project up and running on your local machine.

### 1. Prerequisites

- Python 3.10 or newer
- A Google API Key with the "Generative Language API" enabled. You can get one from [Google AI Studio](https://makersuite.google.com/app/apikey).

### 2. Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd Ovarian-Cyst-Detection
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # For Linux/macOS
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### 3. Configuration

1.  Create a file named `.env` in the root directory of the project.
2.  Add your Google API key to this file. It should contain exactly one line:

    ```
    GOOGLE_API_KEY=YOUR_ACTUAL_API_KEY_HERE
    ```
    *Note: Do not use quotes or spaces around the key.*

### 4. Running the Application

Once the installation and configuration are complete, start the FastAPI server using Uvicorn:

```bash
uvicorn main:app --reload
```

The `--reload` flag enables hot-reloading, so the server will restart automatically when you make code changes.

You can now access the API:
- **Interactive Docs (Swagger UI)**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Alternative Docs (ReDoc)**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## 📖 API Usage

You can use the interactive `/docs` page to test the endpoints or use a tool like `curl` or Postman.

### 1. AI Chatbot Endpoint

Ask a question about the ovarian cyst dataset.

- **Endpoint:** `POST /chatbot`
- **Request Body:**
  ```json
  {
    "question": "How many patients from Eldoret are recommended for surgery?"
  }
  ```
- **Example `curl` command:**
  ```bash
  curl -X 'POST' \
    'http://127.0.0.1:8000/chatbot' \
    -H 'Content-Type: application/json' \
    -d '{
    "question": "How many patients from Eldoret are recommended for surgery?"
  }'
  ```
- **Success Response:**
  ```json
  {
    "answer": "Certainly! According to the dataset, there are 2 patients from the Eldoret region who are recommended for surgery.",
    "sample_questions": [
        "How many patients are from the Nairobi region?",
        ...
    ]
  }
  ```

### 2. ML Prediction Endpoint

Get a recommended management plan for a single patient.

- **Endpoint:** `POST /predict`
- **Request Body:**
  ```json
  {
    "Age": 59,
    "Menopause_Status": "Post-menopausal",
    "Cyst_Size_cm": 2.2,
    "Cyst_Growth_Rate_cm_month": 0.5,
    "CA_125_Level": 123,
    "Ultrasound_Features": "Hemorrhagic cyst",
    "Reported_Symptoms": "Pelvic pain, Irregular periods, Bloating"
  }
  ```
- **Success Response:**
  ```json
  {
    "recommended_management": "Referral"
  }
  ```

## 🚑 Troubleshooting

If you encounter issues, check these common problems first.

- **Problem:** `FATAL ERROR: Failed to load prediction model artifacts... InconsistentVersionWarning`
  - **Cause:** The `ovarian_cyst_inference_artifacts.joblib` file was created with a different version of `scikit-learn` than the one in your environment.
  - **Solution (Recommended):** Re-run the Jupyter Notebook or Python script that was used to train the model. This will generate a new, compatible `.joblib` file.
  - **Solution (Quick Fix):** Downgrade your scikit-learn version to match the one the model was saved with (e.g., `pip install scikit-learn==1.6.1`).

- **Problem:** The chatbot returns an error about not being configured.
  - **Cause:** The application cannot find the data file or the API key.
  - **Solution:**
    1. Ensure you have a directory named `data` in the project root.
    2. Ensure the dataset `Ovarian_Cyst_Track_Data.csv` is inside the `data` directory.
    3. Double-check that your `.env` file exists and contains a valid `GOOGLE_API_KEY`.

- **Problem:** `ModuleNotFoundError` when starting the server.
  - **Cause:** Python cannot find the custom modules (`api`, `models`, etc.).
  - **Solution:** Ensure that every custom directory (`api`, `core`, `models`, `services`) contains an empty `__init__.py` file. This tells Python to treat them as importable packages.