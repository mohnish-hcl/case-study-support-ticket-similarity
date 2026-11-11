import os

from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    url_for
)

from langchain_ollama import (
    ChatOllama
)

from services.config import (
    OLLAMA_LLM_MODEL
)

from services.router import (
    QueryRouter
)

from services.memory import (
    add_user_message,
    add_assistant_message
)

from services.ingest import (
    TicketIngestionService
)

from services.retriever import (
    RetrievalService
)

from services.llm_service import (
    LLMService
)

# ====================================
# APP SETUP
# ====================================

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

# ====================================
# GENERAL CHAT LLM
# ====================================

chat_llm = ChatOllama(
    model=OLLAMA_LLM_MODEL,
    temperature=0.5
)

# ====================================
# HOME
# ====================================

@app.route("/")
def home():

    return redirect(
        url_for("chat")
    )

# ====================================
# CHAT PAGE
# ====================================

@app.route("/chat")
def chat():

    return render_template(
        "chat.html"
    )

# ====================================
# DATASET UPLOAD
# ====================================

@app.route(
    "/upload",
    methods=["POST"]
)
def upload():

    if "file" not in request.files:

        return jsonify({

            "success": False,

            "message": "No file uploaded"
        }), 400

    file = request.files["file"]

    if file.filename == "":

        return jsonify({

            "success": False,

            "message": "Empty filename"
        }), 400

    path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    file.save(path)

    result = (
        TicketIngestionService
        .ingest_json(path)
    )

    return jsonify({

    "success": True,

    "count":
        result["count"]
})

# ====================================
# SEARCH / CHAT
# ====================================

@app.route(
    "/search",
    methods=["POST"]
)
def search():

    body = request.json

    query = body.get(
        "message",
        ""
    ).strip()

    if not query:

        return jsonify({

            "status":
                "ERROR",

            "message":
                "Query cannot be empty"
        })

    add_user_message(
        query
    )

    # -------------------------------
    # ROUTE REQUEST
    # -------------------------------

    intent = (
        QueryRouter.classify(
            query
        )
    )

    print(
        f"Intent Detected: "
        f"{intent}"
    )

    # -------------------------------
    # NORMAL CHAT
    # -------------------------------

    if intent == "CHAT":

        prompt = f"""
You are a friendly
Support Ticket Assistant.

Capabilities:

- Search historical tickets
- Find similar incidents
- Suggest resolutions
- Answer support workflow questions

User Message:

{query}

Be helpful and concise.
"""

        response = (
            chat_llm.invoke(
                prompt
            )
        )

        assistant_message = (
            response.content
        )

        add_assistant_message(
            assistant_message
        )

        return jsonify({

            "status":
                "CHAT",

            "response":
                assistant_message
        })

    # -------------------------------
    # VECTOR SEARCH
    # -------------------------------

    search_result = (
        RetrievalService.search(
            query
        )
    )

    # -------------------------------
    # NO RESULTS
    # -------------------------------

    if (
        search_result["status"]
        == "NO_MATCH"
    ):

        add_assistant_message(
            search_result["message"]
        )

        return jsonify({

            "status":
                "NO_MATCH",

            "message":
                search_result["message"],

            "matches":
                []
        })

    # -------------------------------
    # LLM RESPONSE
    # -------------------------------

    llm_response = (
        LLMService.generate_response(
            query,
            search_result["matches"]
        )
    )

    add_assistant_message(
        llm_response
    )

    return jsonify({

        "status":
            "MATCH_FOUND",

        "llm_response":
            llm_response,

        "matches":
            search_result["matches"]
    })

# ====================================
# START APP
# ====================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )