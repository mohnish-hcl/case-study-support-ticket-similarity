from langchain_ollama import ChatOllama
from services.config import OLLAMA_LLM_MODEL

router_llm = ChatOllama(
    model=OLLAMA_LLM_MODEL,
    temperature=0
)


class QueryRouter:

    @staticmethod
    def classify(query: str, history: str):

        prompt = f"""
        You are a routing agent.

        Conversation History:
        {history}

        Current User Message:
        {query}

        Decide whether historical ticket search is needed.

        Return ONLY one word:

        CHAT
        SEARCH

        Use CHAT for:
        - greetings
        - small talk
        - thank you
        - general discussion
        - follow up answerable from history

        Use SEARCH for:
        - customer issues
        - incidents
        - troubleshooting
        - bugs
        - login problems
        - API issues
        - dashboard failures
        - support requests
        - resolution recommendations
        """

        response = router_llm.invoke(prompt)

        result = response.content.strip().upper()

        if result not in ["CHAT", "SEARCH"]:
            return "SEARCH"

        return result