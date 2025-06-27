# File: services/chatbot_service.py

import pandas as pd
import google.generativeai as genai
from core.config import settings

class ChatbotService:
    def __init__(self, data_path: str):
        # --- THE FIX STARTS HERE ---
        self.df = None
        self.model = None
        self.data_context = ""
        self.error_message = None
        # 1. Initialize is_configured to False
        self.is_configured = False

        # Load the dataset
        try:
            self.df = pd.read_csv(data_path)
            self.data_context = self.df.to_string()
            print("Chatbot data context loaded successfully.")
        except FileNotFoundError:
            self.error_message = f"Data file not found at path: '{data_path}'."
            print(f"ERROR: {self.error_message}")
            return # Stop initialization

        # Configure the Gemini model
        if not settings.GOOGLE_API_KEY or settings.GOOGLE_API_KEY == "YOUR_GOOGLE_API_KEY_NOT_SET":
            self.error_message = "GOOGLE_API_KEY is not set in the .env file."
            print(f"ERROR: {self.error_message}")
            return

        try:
            genai.configure(api_key=settings.GOOGLE_API_KEY)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
            print("Gemini model configured successfully.")
            # 2. Set is_configured to True ONLY if everything succeeds
            self.is_configured = True
        except Exception as e:
            self.error_message = f"Failed to configure Gemini model. Error: {e}"
            print(f"ERROR: {self.error_message}")
            return

    def get_error_details(self) -> str:
        """Returns the specific error that occurred during initialization."""
        return self.error_message or "Chatbot is not configured due to an unknown error."

    def get_answer(self, question: str) -> str:
        """Generates an answer using the configured Gemini model."""
        if not self.is_configured:
            return self.get_error_details()

        prompt = f"""
        You are a friendly medical data assistant. Answer questions based ONLY on the dataset provided.
        Be conversational.

        **Dataset:**
        ```
        {self.data_context}
        ```

        **User's Question:**
        "{question}"

        **Your Conversational Answer:**
        """

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"An error occurred while communicating with the AI model: {e}"

# Create the singleton instance for the app to use
chatbot_service = ChatbotService(data_path=settings.DATA_PATH)