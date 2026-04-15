---
name: lightrag-query
description: Query a LightRAG knowledge base from Claude Code. Use this skill whenever the user wants to ask their knowledge base a question, search their knowledge graph, query LightRAG, or retrieve information from their indexed documents. Triggers on phrases like "ask my knowledge base", "query lightrag", "search my documents", "what does my KB say about", or any request to retrieve information from a LightRAG instance.
---

# LightRAG Query

Query your LightRAG knowledge base via the REST API and return a formatted answer with source references.

## How it works

Send a POST request to the LightRAG server's `/query` endpoint.

## Configuration

- **LightRAG server:** `http://localhost:9621` (default)
- If the server is on a different host/port, adjust the URL below

## Usage

When the user asks a question about their knowledge base, run:

```bash
curl -s -X POST http://localhost:9621/query \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"USER_QUESTION_HERE\", \"mode\": \"hybrid\"}"
```

### Query Modes

The user can optionally specify a mode:
- `hybrid` (default, recommended) — combines local entity relationships + global graph traversal
- `naive` — basic vector similarity search only (like traditional RAG)
- `local` — focuses on immediate entity relationships
- `global` — high-level knowledge retrieval across the entire graph
- `mix` — knowledge graph + vector retrieval combined (best with reranker)

If the user doesn't specify a mode, always use `hybrid`.

### Handling the Response

The response is JSON with two fields:
- `response` — the answer text (markdown formatted)
- `references` — array of source documents that contributed to the answer

Format the output for the user as:
1. The answer text
2. A "Sources" section listing the referenced documents

### Example

User: "What's the relationship between Anthropic and Claude Code?"

```bash
curl -s -X POST http://localhost:9621/query \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"What is the relationship between Anthropic and Claude Code?\", \"mode\": \"hybrid\"}"
```

### Error Handling

- If the server is unreachable, tell the user to check that Docker is running and the LightRAG container is up (`docker ps`)
- If the response is empty or unhelpful, suggest trying a different query mode
