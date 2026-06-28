import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    MODEL_NAME = os.getenv(
        "MODEL_NAME",
        "llama-3.3-70b-versatile"
    )

    EMBEDDING_MODEL = "all-MiniLM-L6-v2"

    CHROMA_PATH = "chroma_db"

    COLLECTION_NAME = "notes"

    CHUNK_SIZE = 500

    CHUNK_OVERLAP = 100