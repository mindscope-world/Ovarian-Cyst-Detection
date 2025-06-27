# services/chatbot_service.py

# File: services/chatbot_service.py

import pandas as pd
import google.generativeai as genai
from core.config import settings

class ChatbotService:
    def __init__(self, data_path: str):
        self.model = None
        self.df = None
        self.data_context = "Data not available."
        
        # 1. Load the dataset
        try:
            self.df = pd.read_csv(data_path)
            # Convert the entire dataframe to a string to be used as context
            self.data_context = self.df.to_string()
            print("Chatbot data context loaded successfully.")
        except FileNotFoundError:
            print(f"ERROR: Chatbot data file not found at {data_path}. The chatbot will not work.")
            return # Stop initialization if data is not found

        # 2. Configure the Gemini model
        if settings.GOOGLE_API_KEY and settings.GOOGLE_API_KEY != "YOUR_GOOGLE_API_KEY_NOT_SET":
            try:
                genai.configure(api_key=settings.GOOGLE_API_KEY)
                self.model = genai.GenerativeModel('gemini-2.5-flash')
                print("Gemini model configured successfully.")
            except Exception as e:
                print(f"ERROR: Failed to configure Gemini model: {e}")
        else:
             print("WARNING: GOOGLE_API_KEY is not set. The chatbot will not work.")

    def get_answer(self, question: str) -> str:
        if self.model is None or self.df is None:
            return "Chatbot is not configured properly. Please check the data file path and ensure the GOOGLE_API_KEY is set in your .env file."

        prompt = f"""
        You are an expert medical data analyst. Your sole task is to answer questions based ONLY on the dataset provided below.

        **Dataset:**
        ```
        {self.data_context}
        ```

        **Instructions:**
        1.  Analyze the dataset to answer the user's question.
        2.  Do NOT use any external knowledge.
        3.  If the answer cannot be found in the dataset, state that the information is not available in the provided data.
        4.  Provide concise and direct answers. For calculations (e.g., average, count), perform them and state the result.

        **User's Question:**
        "{question}"

        **Answer:**
        """

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"An error occurred while communicating with the AI model: {e}"

# Create a singleton instance that will be loaded on application startup
# and imported by the API endpoint.
chatbot_service = ChatbotService(data_path=settings.DATA_PATH)