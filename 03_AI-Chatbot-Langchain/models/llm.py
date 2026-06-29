from langchain_groq import ChatGroq
from config import Config

class LLMFactory:
    @staticmethod
    def create():
        return ChatGroq(
            api_key = Config.GROQ_API_KEY,
            model = Config.MODEL_NAME,
            temperature = 0
        )