from langchain_ollama import ChatOllama
from services.config import OLLAMA_LLM_MODEL

llm = ChatOllama(model=OLLAMA_LLM_MODEL, temperature=0.2)


class LLMService:

    @staticmethod
    def generate_response(query, matches):
        context = ""

        for match in matches:
            context += f"""
Ticket:
{match['ticket_id']}

Category:
{match['category']}

Tags:
{match['tags']}

Resolution:
{match['resolution']}
"""

        prompt = f"""
You are a support engineer.

Customer Issue:

{query}

Historical Tickets:

{context}

Write ONLY:

A short recommendation
(2-3 sentences maximum).

Do NOT:

- Explain similarity
- Explain your reasoning
- Describe ranking
- Mention confidence
- Repeat ticket details
- Use numbered lists
"""

        response = llm.invoke(prompt)
        return response.content.strip()