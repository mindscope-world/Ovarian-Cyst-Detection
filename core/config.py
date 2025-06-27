# core/config.py

import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

class Settings:
    """
    Application settings loaded from environment variables.
    """
    # Safely get the Google API key, providing a default placeholder
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "YOUR_GOOGLE_API_KEY_NOT_SET")
    
    # Path to the dataset for the chatbot
    DATA_PATH: str = "data/Ovarian_Cyst_Track _Data.csv"

# Create a single, importable instance of the settings
settings = Settings()