import json
from langchain_core.documents import Document
from services.vector_store import vector_store


class TicketIngestionService:

    @staticmethod
    def ingest_json(filepath):
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)

        tickets = data.get("tickets", [])
        documents = []
        ids = []

        for ticket in tickets:
            ticket_id = ticket.get("ticket_id", "")

            document = Document(
                page_content=f"""
Subject:
{ticket.get('subject', '')}

Description:
{ticket.get('description', '')}
""",
                metadata={
                    "ticket_id": ticket_id,
                    "subject": ticket.get("subject", ""),
                    "description": ticket.get("description", ""),
                    "category": ticket.get("category", ""),
                    "tags": ",".join(ticket.get("tags", [])),
                    "status": ticket.get("status", ""),
                    "created_at": ticket.get("created_at", ""),
                    "resolution": ticket.get("resolution_notes", "")
                }
            )

            documents.append(document)
            ids.append(ticket_id)

        collection = vector_store._collection
        existing = collection.get()

        if existing["ids"]:
            collection.delete(ids=existing["ids"])

        vector_store.add_documents(documents=documents, ids=ids)

        return {"count": len(documents)}

    @staticmethod
    def collection_count():
        try:
            return vector_store._collection.count()
        except:
            return 0