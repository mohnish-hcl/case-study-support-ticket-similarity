# Support Ticket Similarity Assistant

## Overview

This project implements a Support Ticket Similarity Assistant for Solari Analytics.

The application helps support engineers identify previously resolved tickets that are semantically similar to newly reported customer issues.

The assistant supports conversational interactions, maintains short-term conversation memory, automatically determines when historical ticket retrieval is required, and generates recommendations using retrieved ticket knowledge.

Historical tickets are embedded and indexed in ChromaDB. Incoming support queries are compared against historical incidents and the most relevant tickets, resolutions, categories, and tags are returned.

---

## Technology Stack

- Python
- Flask
- LangChain
- ChromaDB
- Ollama
- nomic-embed-text (Embeddings)
- phi4-mini (Routing, Query Rewriting, and Response Generation)

---

## Architecture

```text
User Query
        │
        ▼
Conversation History
        │
        ▼
LLM Router
        │
 ┌──────┴──────┐
 │             │
 ▼             ▼

CHAT        SEARCH
 │             │
 ▼             ▼

Phi4      Query Rewriter
Response         │
                 ▼
         Nomic Embed Text
                 │
                 ▼
      ChromaDB Similarity Search
                 │
                 ▼
        Top Historical Tickets
                 │
                 ▼
        Phi4 Mini Recommendation
                 │
                 ▼
        Similar Ticket Listing
```

Conversation history is maintained and reused across interactions to support follow-up questions and context-aware retrieval.

---

## Prerequisites

### Python

Recommended:

```bash
Python 3.11+
```

Verify:

```bash
python --version
```

---

## Install Ollama

Download:

https://ollama.com/download

Verify installation:

```bash
ollama --version
```

---

## Download Required Models

### Embedding Model

```bash
ollama pull nomic-embed-text
```

### LLM

```bash
ollama pull phi4-mini
```

Verify:

```bash
ollama list
```

Expected:

```text
nomic-embed-text
phi4-mini
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Configuration

Create a `.env` file:

```env
ollama_embedding_model=nomic-embed-text
ollama_llm_model=phi4-mini
CHROMA_PATH=./chroma_db
MAX_CHAT_HISTORY=20
CONFIDENCE_THRESHOLD=60
TOP_K_RESULTS=3
```

---

## Run The Application

```bash
python app.py
```

Application URL:

```text
http://localhost:5000
```

---

## Using The Application

### Step 1

Upload `tickets.json`.

The application will:

- Read historical tickets
- Generate embeddings using `nomic-embed-text`
- Build the ChromaDB vector index
- Enable semantic retrieval

### Step 2

Ask support questions.

Examples:

```text
Customer charged twice for subscription renewal.
Password reset email never arrives.
Revenue dashboard shows blank page.
API returning HTTP 429 errors.
```

### Conversational Support

The assistant supports multi-turn conversations.

Example:

```text
User:
Customer cannot login.

Assistant:
Can you provide the error message?

User:
500 Internal Server Error.
```

The assistant uses conversation history to understand follow-up questions and improve retrieval accuracy.

### Step 3

Review the AI recommendation.

### Step 4

Review historical tickets including:

- Ticket ID
- Subject
- Description
- Category
- Tags
- Resolution Notes
- Confidence Score

---

## Retrieval Workflow

### Step 1

User submits a support question.

Example:

```text
Customer charged twice this month.
```

### Step 2

Conversation history is collected.

### Step 3

The LLM Router determines whether historical ticket retrieval is required.

### Step 4

If retrieval is required, the Query Rewriter converts the latest message into a standalone search query.

Example:

```text
Original:
What about SSO users?

Rewritten:
Customer login failures affecting SSO users.
```

### Step 5

The rewritten query is embedded using `nomic-embed-text`.

### Step 6

ChromaDB retrieves the most relevant historical tickets.

### Step 7

Retrieved tickets are sent to Phi4 Mini along with the conversation history.

### Step 8

Phi4 Mini generates a concise recommendation while ticket details are displayed in the UI.

---

## Design Decisions

### Why Semantic Search?

Keyword matching struggles with:

```text
Cannot login
```

vs

```text
Authentication failure
```

Semantic embeddings capture meaning rather than exact words.

### Why Conversation Memory?

Support investigations are rarely a single question-and-answer interaction.

Conversation history is provided to:

- LLM routing
- Query rewriting
- Recommendation generation

This allows the assistant to understand references such as:

```text
it
that issue
same customer
will the same fix work?
```

without requiring users to repeat previous context.

### Why Query Rewriting?

Follow-up questions often lack enough information for effective retrieval.

Example:

```text
Customer cannot login.
```

Followed by:

```text
What about SSO users?
```

Before retrieval, the latest user message is rewritten into a standalone search query using conversation history.

Benefits:

- Better retrieval accuracy
- Improved follow-up handling
- Reduced ambiguity

### Why ChromaDB?

- Lightweight
- Local vector store
- Fast retrieval
- Easy LangChain integration

### Why Ollama?

- Fully local deployment
- No API keys required
- No recurring cost
- Offline capable after model download

### Why Nomic Embed Text?

Purpose-built embedding model optimized for semantic retrieval.

### Why Phi4 Mini?

Phi4 Mini is used for:

- Query routing
- Query rewriting
- Recommendation generation
- Conversational responses

Retrieval and generation remain separate, reducing hallucination risk while maintaining conversational flexibility.

---

## Confidence Filtering

Confidence Threshold:

```text
60%
```

Historical tickets below the configured threshold are not returned.

---

## Known Limitations

- Uses uploaded JSON instead of live ticket system integrations.
- Conversation memory is stored in application memory and is cleared when the application restarts.
- Small synthetic dataset.
- No user-feedback ranking loop.
- No hybrid keyword + semantic retrieval.
- No persistent user sessions.

---

## Future Work

- Persistent conversation storage (PostgreSQL / SQL Server)
- Session-based memory
- Recency-aware ranking
- Category-aware filtering
- Hybrid retrieval and reranking
- Feedback learning
- ServiceNow integration
- Zendesk integration
- Jira Service Management integration
- Azure OpenAI embeddings
- Multi-tenant support

---

## Demo Flow

1. Upload `tickets.json`
2. Wait for indexing
3. Ask a support question
4. Assistant determines whether retrieval is required
5. Historical tickets are retrieved when appropriate
6. Review AI recommendation
7. Continue the conversation naturally with follow-up questions
8. Review supporting historical tickets and resolutions