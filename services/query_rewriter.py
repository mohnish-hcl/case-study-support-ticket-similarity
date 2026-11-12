from langchain_ollama import ChatOllama
from services.config import OLLAMA_LLM_MODEL

rewriter_llm = ChatOllama(
    model=OLLAMA_LLM_MODEL,
    temperature=0
)


class QueryRewriter:

    @staticmethod
    def rewrite(query, history):

        prompt = f"""
        You are a search query optimizer.

        Conversation:
        {history}

        Current User Message:
        {query}

        Rewrite the latest user message into a
        standalone search query suitable for
        ticket retrieval.

        Return ONLY the rewritten query.
        """

        response = rewriter_llm.invoke(prompt)

        return response.content.strip()