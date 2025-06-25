# Ovarian Cyst Management Prediction API

This project provides a **FastAPI-based web service** for predicting the recommended management of ovarian cysts based on patient data. It loads a machine learning model and preprocessing artifacts, exposes a `/predict` endpoint, and is ready for deployment on [Render.com](https://render.com/) or any cloud platform.

## 🚀 Features

- **Machine Learning Model**: Predicts recommended management for ovarian cysts
- **Preprocessing**: Handles categorical, numerical, and multi-label features as in training
- **REST API**: Accepts JSON input, returns prediction as JSON
- **Ready for Cloud**: Binds to `0.0.0.0` and uses the `PORT` environment variable (required by Render)
- **Easy to Extend**: Modular code structure for adding new features or endpoints

## 🏗️ Project Structure

```
.
├── ovarian_cyst_inference_artifacts.joblib   # Model & preprocessing artifacts
├── ovarian_cyst_api.py                       # Main FastAPI app (rename as needed)
├── requirements.txt                          # Python dependencies
└── README.md                                 # This file
```

## 📝 API Usage

### **Endpoint**

`POST /predict`

### **Request Body Example**

```json
{
  "Age": 45,
  "Menopause_Status": "Pre-menopausal",
  "Cyst_Size_cm": 4.2,
  "Cyst_Growth_Rate_cm_month": 0.3,
  "CA_125_Level": 35,
  "Ultrasound_Features": "Simple cyst",
  "Reported_Symptoms": "Pelvic pain, Nausea"
}
```

### **Response Example**

```json
{
  "recommended_management": "Follow-up ultrasound in 6 months"
}
```

## ⚙️ Setup & Deployment

### 1. **Clone the Repository**

```bash
git clone https://github.com/yourusername/ovarian-cyst-api.git
cd ovarian-cyst-api
```

### 2. **Install Dependencies**

```bash
pip install -r requirements.txt
```

### 3. **Ensure Model Artifacts Are Present**

Place `ovarian_cyst_inference_artifacts.joblib` in the same directory as your API script.

### 4. **Run Locally**

```bash
python ovarian_cyst_api.py
```

The API will be available at `http://localhost:8000`.

### 5. **Deploy to Render.com**

- Push your code to a GitHub repository.
- Create a new **Web Service** on Render.
- Set the **Start Command** to:
  ```
  python ovarian_cyst_api.py
  ```
- Render will set the `PORT` environment variable automatically.
- Your API will be available at your Render service URL.

## 🛠️ Technical Notes

- **Port Binding**: The app binds to `0.0.0.0` and uses the `PORT` env variable for compatibility with Render and other cloud platforms.
- **Model Artifacts**: The `ovarian_cyst_inference_artifacts.joblib` file must include:
  - The trained model (`model`)
  - MultiLabelBinarizer (`mlb_encoder`)
  - Feature names and encodings (`symptom_column_names`, `ultrasound_one_hot_columns`, `pipeline_input_columns`, etc.)
- **Preprocessing**: The input is preprocessed to match the format expected by the model pipeline.

## 🧑‍💻 Development

- **Add new endpoints** by following FastAPI conventions.
- **Retrain or update the model** and save new artifacts as `ovarian_cyst_inference_artifacts.joblib`.

## 📚 References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Render.com Web Services](https://render.com/docs/web-services)
- [Uvicorn ASGI Server](https://www.uvicorn.org/)

## 📝 License

MIT License (or specify your license)

## 🙋‍♀️ Questions?

Open an issue or contact [your-email@example.com](mailto:your-email@example.com).

**Happy predicting!**