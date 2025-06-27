Of course. Here is the updated `README.md` file with a new "Deployment" section that includes detailed, step-by-step instructions for deploying the application to Render.

This new section is placed right after the "Getting Started" guide, which is a logical place for it.

---

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
├── build.sh              # Deployment build script for Render
├── requirements.txt      # Project dependencies
├── ovarian_cyst_inference_artifacts.joblib # The trained ML model
|
├── data/
│   └── Ovarian_Cyst_Track_Data.csv  # The dataset for the chatbot
|
├── api/                  # API endpoint definitions (routers)
│   ├── ...
|
├── services/             # Business logic (e.g., calling Gemini)
│   ├── ...
|
├── core/                 # Application configuration
│   ├── ...
|
└── models/               # Pydantic data models (schemas)
    ├── ...
```

## 🚀 Getting Started (Local Development)

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

The `--reload` flag enables hot-reloading for development. You can now access the API locally:
- **Interactive Docs (Swagger UI)**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Alternative Docs (ReDoc)**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## ☁️ Deployment (to Render)

This application is ready to be deployed for free on [Render](https://render.com/).

### 1. Prepare for Deployment

Before deploying, ensure you have the following files in your repository root:

1.  **`requirements.txt`**: This file lists all necessary Python packages. If it's missing or outdated, generate it with:
    ```bash
    pip freeze > requirements.txt
    ```
2.  **`build.sh`**: A build script for Render. Create this file and add the following:
    ```sh
    #!/usr/bin/env bash
    # exit on error
    set -o errexit

    pip install -r requirements.txt
    ```
3.  Commit and push all your latest changes, including these two files, to your GitHub repository.

### 2. Deploy on Render

1.  **Sign up** on [Render](https://render.com/) using your GitHub account.
2.  On the dashboard, click **New +** > **Web Service**.
3.  **Connect your repository** and select the correct project repo.
4.  **Configure the service** with the following settings:
    - **Name:** A unique name (e.g., `ovarian-cyst-api`).
    - **Region:** Choose a location near you.
    - **Build Command:** `./build.sh`
    - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
    - **Instance Type:** Select the **Free** plan.
5.  **Add Environment Variables:**
    - Scroll down and expand the **Advanced** section.
    - Click **Add Environment Variable**.
    - **Key:** `GOOGLE_API_KEY`, **Value:** `YOUR_ACTUAL_API_KEY_HERE`
    - (Optional) **Key:** `PYTHON_VERSION`, **Value:** `3.12` (or your Python version)
6.  Click **Create Web Service**. Render will automatically build and deploy your application. Once complete, your API will be live at the URL provided on your dashboard.

## 📖 API Usage

You can use the interactive `/docs` page on your live URL to test the endpoints or use a tool like `curl` or Postman.

### 1. AI Chatbot Endpoint

- **Endpoint:** `POST /chatbot`
- **Example `curl` command:**
  ```bash
  curl -X 'POST' \
    'https://your-app-name.onrender.com/chatbot' \
    -H 'Content-Type: application/json' \
    -d '{
    "question": "How many patients from Eldoret are recommended for surgery?"
  }'
  ```

### 2. ML Prediction Endpoint

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

## 🚑 Troubleshooting

- **Problem:** `FATAL ERROR: ... InconsistentVersionWarning`
  - **Cause:** The `.joblib` model file was created with a different `scikit-learn` version.
  - **Solution (Recommended):** Re-run the model training script to generate a new, compatible `.joblib` file and push it to your repository.
  - **Solution (Quick Fix):** Downgrade your scikit-learn version in `requirements.txt` to match the version the model was saved with (e.g., `scikit-learn==1.6.1`).

- **Problem:** Chatbot returns configuration errors.
  - **Solution:**
    1. Ensure the `data/Ovarian_Cyst_Track_Data.csv` file exists in your repository.
    2. Ensure the `GOOGLE_API_KEY` environment variable is set correctly on Render.

- **Problem:** `ModuleNotFoundError` during deployment.
  - **Solution:** Ensure that every custom directory (`api`, `core`, `models`, `services`) contains an empty `__init__.py` file.