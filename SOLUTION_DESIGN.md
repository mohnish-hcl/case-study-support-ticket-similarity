# Solution Design

## Problem Statement

Solari Analytics support agents handle approximately 150 support tickets per day. A recurring challenge is that agents are often unaware that a customer issue has already been investigated and resolved previously.

This results in:

- Slower ticket resolution
- Inconsistent customer guidance
- Duplicate investigation effort

The goal is to surface historical tickets and previous resolutions whenever a similar issue is reported.

---

## Assumptions

### Historical Data Availability

Historical tickets are available as JSON exports.

### Ticket Structure

Each ticket contains:

- Ticket ID
- Subject
- Description
- Category
- Tags
- Resolution Notes

### Similarity Definition

Ticket similarity should be determined primarily using:

- Subject
- Description

### Response Time

Support agents expect recommendations within a few seconds.

### Historical Data Volume

The starter dataset contains approximately 40 historical tickets and is assumed to be a representative sample rather than a production-scale support repository.

Solari Analytics currently handles approximately 150 support tickets per day and expects ticket volume to grow.

For the first version, all historical tickets participate equally in retrieval because the primary requirement is issue similarity rather than recency.

---

## Starter Kit Usage

### data/tickets.json

Contains approximately 40 synthetic historical support tickets.

Each ticket contains:

- Ticket ID
- Subject
- Description
- Category
- Tags
- Resolution Notes
- Created Date
- Status

These tickets form the historical knowledge base indexed into ChromaDB.

### data/new_tickets_example.json

Contains sample incoming support tickets for testing.

The file includes billing, authentication, rendering, export and integration scenarios.

One Snowflake integration example intentionally does not closely resemble the existing historical corpus and was used to validate confidence threshold handling and no-match behaviour.

### ticket_utils.py

The starter utility provides:

- Ticket loading helpers
- Text normalization
- Keyword overlap scoring

The final solution does not use the keyword overlap approach because semantic retrieval was selected instead.

---

## Architecture

User Query
→ Intent Router
→ CHAT or SEARCH

SEARCH:

User Query
→ Nomic Embed Text
→ ChromaDB
→ Similar Historical Tickets
→ Phi4 Mini Recommendation
→ Ticket Listing

---

## Ticket Ingestion Strategy

### Vectorized Content

Only the following fields are embedded:

- Subject
- Description

Reason:

These fields represent the customer issue and provide the strongest similarity signal.

### Metadata

Stored separately:

- Ticket ID
- Category
- Tags
- Resolution Notes
- Status
- Created Date

Reason:

Metadata is useful for display, recommendations and future filters but should not distort semantic similarity calculations.

---

## Retrieval Workflow

### Step 1

User submits issue description.

Example:

Customer charged twice this month.

### Step 2

Query embedding generated using nomic-embed-text.

### Step 3

ChromaDB similarity search retrieves top matching incidents.

### Step 4

Confidence filtering removes weak results.

Configured threshold:

60%

### Step 5

Relevant tickets are passed to Phi4 Mini.

### Step 6

Phi4 generates a short personalized recommendation while historical ticket details are shown directly in the UI.

---

## Why Separate Retrieval and Generation?

Retrieval:

- Nomic Embed Text
- ChromaDB

Generation:

- Phi4 Mini

Benefits:

- Easier debugging
- Better explainability
- Reduced hallucination risk
- Component independence

---

## Trade-Off Analysis

### Option 1: Keyword Search

Pros:

- Simple
- Fast

Cons:

- Misses semantically related issues

Rejected.

### Option 2: Full LLM Search

Pros:

- Flexible

Cons:

- Expensive
- Less deterministic
- Harder to explain

Rejected.

### Option 3: Semantic Retrieval (Chosen)

Pros:

- Captures meaning
- Explainable architecture
- Scalable retrieval pattern
- Works with differently worded issues

Cons:

- Requires embedding generation

Chosen because it best addresses the customer's problem.

### Historical Ticket Age Consideration

Date-based filtering was evaluated but intentionally excluded from Version 1.

Reasons:

- The provided dataset is relatively small.
- Older tickets may still contain useful resolutions.
- The customer requirement focuses on similarity rather than recency.

All historical tickets currently participate equally in retrieval.

---

## Confidence Threshold

Current threshold:

60%

Benefits:

- Reduces noisy matches
- Avoids misleading recommendations
- Helps identify genuinely new issues

---

## Future Improvements

### Recency-Aware Ranking

The dataset contains a created_at field.

A future implementation could incorporate time-based ranking.

Example:

Final Score =
80% Semantic Similarity
+ 20% Recency Weight

Example recency weights:

- Last 30 days → 1.0
- Last 90 days → 0.8
- Last 180 days → 0.6
- Older tickets → 0.4

Benefits:

- Prioritizes recent resolutions
- Reduces outdated recommendations
- Preserves historical knowledge while improving relevance

### Hybrid Retrieval

Combine:

- Semantic Search
- Keyword Search

### Category Filtering

Use category metadata to narrow search scope.

### Agent Feedback Loop

Capture recommendation usefulness to improve ranking.

### Integrations

Potential integrations:

- Zendesk
- ServiceNow
- Salesforce
- Jira Service Management

---

## Conclusion

The implemented solution focuses on retrieving semantically similar historical tickets and surfacing previous resolutions quickly and consistently.

The architecture remains lightweight while providing a clear path toward larger-scale support operations, recency-aware ranking, and future AI enhancements.
