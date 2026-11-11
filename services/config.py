import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_EMBEDDING_MODEL = os.getenv("ollama_embedding_model")
OLLAMA_LLM_MODEL = os.getenv("ollama_llm_model")
CHROMA_PATH = os.getenv("CHROMA_PATH", "./chroma_db")
MAX_CHAT_HISTORY = int(os.getenv("MAX_CHAT_HISTORY", 20))
CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD"))
TOP_K_RESULTS = int(os.getenv("TOP_K_RESULTS", 3))