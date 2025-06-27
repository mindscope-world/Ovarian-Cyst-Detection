Of course. That's an excellent and crucial addition. A user needs to know exactly what data to provide to the prediction endpoint.

I will update the `README.md` to include a detailed table explaining each field for the `/predict` endpoint, including the data type and the specific, allowed string values for categorical features. This makes the documentation much more useful.

Here is the complete, updated `README.md` file. The changes are in the **"API Usage" -> "ML Prediction Endpoint"** section.

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

### 2. Installation & Configuration

1.  **Clone the repository** and navigate into the project directory.
2.  **Create and activate a virtual environment** (e.g., `python3 -m venv venv` and `source venv/bin/activate`).
3.  **Install dependencies:** `pip install -r requirements.txt`.
4.  **Create a `.env` file** in the root directory and add your Google API key: `GOOGLE_API_KEY=YOUR_ACTUAL_API_KEY_HERE`.

### 3. Running the Application

Start the FastAPI server using Uvicorn:

```bash
uvicorn main:app --reload
```

- **Interactive Docs (Swagger UI)**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## ☁️ Deployment (to Render)

This application is ready to be deployed for free on [Render](https://render.com/).

1.  **Prepare:** Make sure you have `requirements.txt` and a `build.sh` file in your repository.
    - `build.sh` should contain:
      ```sh
      #!/usr/bin/env bash
      set -o errexit
      pip install -r requirements.txt
      ```
2.  **Deploy on Render:**
    - Create a new **Web Service** and connect your GitHub repo.
    - **Build Command:** `./build.sh`
    - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
    - **Instance Type:** `Free`
    - **Add Environment Variable:** `GOOGLE_API_KEY` with your key as the value.
    - Click **Create Web Service**.

## 📖 API Usage

You can use the interactive `/docs` page on your live URL to test the endpoints or use a tool like `curl`.

### 1. AI Chatbot Endpoint

- **Endpoint:** `POST /chatbot`
- **Purpose:** Ask a natural language question about the ovarian cyst dataset.

### 2. ML Prediction Endpoint

- **Endpoint:** `POST /predict`
- **Purpose:** Get a recommended management plan for a single patient based on clinical features.

The endpoint requires a JSON object with the following fields:

| Field                       | Data Type | Description / Valid Values                                                                                             |
| :-------------------------- | :-------- | :--------------------------------------------------------------------------------------------------------------------- |
| `Age`                       | `integer` | The patient's age in years.                                                                                            |
| `Menopause_Status`          | `string`  | The patient's menopausal status. **Must be one of:**<br>`"Pre-menopausal"` or `"Post-menopausal"`                          |
| `Cyst_Size_cm`              | `float`   | The size of the cyst in centimeters (e.g., `5.5`).                                                                     |
| `Cyst_Growth_Rate_cm_month` | `float`   | The rate of cyst growth per month (e.g., `0.5`).                                                                       |
| `CA_125_Level`              | `integer` | The CA 125 cancer antigen level.                                                                                       |
| `Ultrasound_Features`       | `string`  | The observed features from the ultrasound. **Must be one of:**<br>`"Simple cyst"`, `"Complex cyst"`, `"Septated cyst"`, `"Hemorrhagic cyst"`, `"Solid mass"` |
| `Reported_Symptoms`         | `string`  | A single, comma-separated string of symptoms. Can be an empty string (`""`) if there are no symptoms.<br>_Example: `"Pelvic pain, Nausea, Bloating"`_ |

<br>

**Example Request Body:**

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

**Success Response:**

```json
{
  "recommended_management": "Referral"
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