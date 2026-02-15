import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

class ModelFactory:
    @staticmethod
    def create_model(temperature=0.0):
        """Returns a configured Gemini 1.5 Flash instance."""
        return ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=temperature
        )