import os
from flask import Flask, render_template, request, jsonify, redirect, url_for
from langchain_ollama import ChatOllama

from services.config import OLLAMA_LLM_MODEL
from services.router import QueryRouter
from services.memory import add_user_message, add_assistant_message, build_history_text
from services.ingest import TicketIngestionService
from services.retriever import RetrievalService
from services.llm_service import LLMService
from services.query_rewriter import QueryRewriter
# ====================================
# APP SETUP
# ====================================
app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

chat_llm = ChatOllama(model=OLLAMA_LLM_MODEL, temperature=0.5)

# ====================================
# ROUTES
# ====================================
@app.route("/")
def home():
    return redirect(url_for("chat"))

@app.route("/chat")
def chat():
    return render_template("chat.html")

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"success": False, "message": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"success": False, "message": "Empty filename"}), 400

    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    result = TicketIngestionService.ingest_json(path)
    return jsonify({"success": True, "count": result["count"]})

@app.route("/search", methods=["POST"])
def search():

    body = request.json or {}

    query = body.get("message", "").strip()

    if not query:
        return jsonify({
            "status": "ERROR",
            "message": "Query cannot be empty"
        })

    add_user_message(query)

    history = build_history_text()

    intent = QueryRouter.classify(
        query=query,
        history=history
    )

    print(f"ROUTER DECISION: {intent}")

    if intent == "CHAT":

        prompt = f"""
You are a friendly Support Assistant.

Conversation History:
{history}

Current User Message:
{query}

Respond naturally.
"""

        response = chat_llm.invoke(prompt)

        assistant_message = response.content

        add_assistant_message(
            assistant_message
        )

        return jsonify({
            "status": "CHAT",
            "response": assistant_message
        })

    search_query = QueryRewriter.rewrite(
        query=query,
        history=history
    )

    print(f"REWRITTEN QUERY: {search_query}")

    search_result = RetrievalService.search(
        search_query
    )

    if search_result["status"] == "NO_MATCH":

        fallback_prompt = f"""
Conversation:
{history}

User:
{query}

No ticket matches were found.

Provide the best possible assistance.
"""

        response = chat_llm.invoke(
            fallback_prompt
        )

        answer = response.content

        add_assistant_message(answer)

        return jsonify({
            "status": "CHAT",
            "response": answer
        })

    llm_response = (
        LLMService.generate_response(
            query=query,
            matches=search_result["matches"],
            history=history
        )
    )

    add_assistant_message(
        llm_response
    )

    return jsonify({
        "status": "MATCH_FOUND",
        "llm_response": llm_response,
        "matches": search_result["matches"]
    })
# ====================================
# START APP
# ====================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)