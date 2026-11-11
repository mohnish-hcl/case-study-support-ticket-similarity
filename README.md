# Support Ticket Similarity Assistant

## Overview

This project implements a Support Ticket Similarity Assistant for Solari Analytics.

The application helps support engineers quickly identify previously resolved tickets that are semantically similar to newly reported customer issues. Historical tickets are embedded and indexed in ChromaDB. Incoming support queries are compared against historical incidents and the most relevant tickets, resolutions, categories and tags are returned.

## Technology Stack

- Python
- Flask
- LangChain
- ChromaDB
- Ollama
- nomic-embed-text (Embeddings)
- phi4-mini (LLM)

---

## Architecture

User Query
→ Intent Router
→ CHAT or SEARCH

SEARCH:

User Query
→ Nomic Embed Text
→ ChromaDB Similarity Search
→ Top Historical Tickets
→ Phi4 Mini Recommendation
→ Similar Ticket Listing

---

## Prerequisites

### Python

Recommended:

Python 3.11+

Verify:

python --version

---

## Install Ollama

Download:

https://ollama.com/download

Verify installation:

ollama --version

---

## Download Required Models

Embedding Model:

ollama pull nomic-embed-text

LLM:

ollama pull phi4-mini

Verify:

ollama list

Expected:

nomic-embed-text
phi4-mini

---

## Create Virtual Environment

Windows:

python -m venv venv

Activate:

venv\Scripts\activate

---

## Install Dependencies

pip install -r requirements.txt

---

## Environment Configuration

Create a .env file:

ollama_embedding_model=nomic-embed-text
ollama_llm_model=phi4-mini
CHROMA_PATH=./chroma_db
MAX_CHAT_HISTORY=20
CONFIDENCE_THRESHOLD=60
TOP_K_RESULTS=3

---

## Run The Application

python app.py

Application URL:

http://localhost:5000

---

## Using The Application

### Step 1

Upload tickets.json.

The application will:

- Read historical tickets
- Generate embeddings using nomic-embed-text
- Build the ChromaDB vector index
- Enable semantic retrieval

### Step 2

Ask support questions.

Examples:

Customer charged twice for subscription renewal.

Password reset email never arrives.

Revenue dashboard shows blank page.

API returning HTTP 429 errors.

### Step 3

Review AI recommendation.

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

## Confidence Filtering

Confidence Threshold:

60%

Historical tickets below the configured threshold are not returned.

---

## Design Decisions

### Why Semantic Search?

Keyword matching struggles with:

Cannot login

vs

Authentication failure

Semantic embeddings capture meaning rather than exact words.

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

Purpose-built embedding model used for retrieval.

### Why Phi4 Mini?

Used only for recommendations and conversational responses.

Retrieval and generation remain separate.

---

## Known Limitations

- Uses uploaded JSON instead of live ticket system integrations.
- Small synthetic dataset.
- No user-feedback ranking loop.
- No hybrid keyword + semantic retrieval.

---

## Future Work

- Category-aware filtering
- Hybrid retrieval
- Feedback learning
- ServiceNow integration
- Zendesk integration
- Azure OpenAI embeddings
- Multi-tenant support

---

## Demo Flow

1. Upload tickets.json
2. Wait for indexing
3. Ask support question
4. Read recommendation
5. Review similar historical tickets
6. Use historical resolutions to assist customers
