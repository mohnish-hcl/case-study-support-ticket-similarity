from services.vector_store import vector_store
from services.config import (
    TOP_K_RESULTS,
    CONFIDENCE_THRESHOLD
)


class RetrievalService:

    @staticmethod
    def search(query):

        results = vector_store.similarity_search_with_relevance_scores(
            query=query,
            k=TOP_K_RESULTS
        )

        matches = []

        for doc, score in results:

            confidence = round(score * 100, 2)

            if confidence < CONFIDENCE_THRESHOLD:
                continue

            matches.append({
                "ticket_id": doc.metadata.get("ticket_id"),
                "subject": doc.metadata.get("subject"),
                "description": doc.metadata.get("description"),
                "category": doc.metadata.get("category"),
                "tags": doc.metadata.get("tags"),
                "status": doc.metadata.get("status"),
                "created_at": doc.metadata.get("created_at"),
                "resolution": doc.metadata.get("resolution"),
                "confidence": confidence
            })

        return {
            "status": "MATCH_FOUND" if matches else "NO_MATCH",
            "matches": matches
        }