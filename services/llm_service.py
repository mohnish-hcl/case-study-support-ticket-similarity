from langchain_ollama import ChatOllama
from services.config import OLLAMA_LLM_MODEL

llm = ChatOllama(
    model=OLLAMA_LLM_MODEL,
    temperature=0.2
)


class LLMService:

    @staticmethod
    def generate_response(query,matches,history):
        context = ""
        for match in matches:

            context += f"""
            Ticket ID: {match['ticket_id']}
            Subject: {match['subject']}
            Category: {match['category']}
            Resolution: {match['resolution']}

            """

        prompt = f"""
        You are an experienced Support Engineer.

        Conversation History:
        {history}

        Current User Query:
        {query}

        Historical Ticket Context:
        {context}

        Instructions:

        - Understand conversation history.
        - Use historical tickets if relevant.
        - Recommend likely resolution.
        - Keep response under 5 sentences.
        - Do not mention confidence scores.
        - Do not explain retrieval process.
        """

        response = llm.invoke(prompt)

        return response.content.strip()