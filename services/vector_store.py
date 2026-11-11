from langchain_chroma import Chroma

from langchain_ollama import (
    OllamaEmbeddings
)

from services.config import (
    OLLAMA_EMBEDDING_MODEL,
    CHROMA_PATH
)

embeddings = OllamaEmbeddings(
    model=OLLAMA_EMBEDDING_MODEL
)

vector_store = Chroma(
    collection_name="support_tickets",
    persist_directory=CHROMA_PATH,
    embedding_function=embeddings
)