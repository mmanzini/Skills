---
name: lightrag-status
description: Check the status of a LightRAG knowledge base — documents indexed, processing status, and top entities. Use this skill whenever the user wants to know the state of their knowledge base, check if documents are still processing, see what's been indexed, or get a health check on their LightRAG instance. Triggers on phrases like "lightrag status", "what's in my knowledge base", "is lightrag still processing", "how many documents are indexed", or any request to check the state of a LightRAG instance.
---

# LightRAG Status

Get a quick health check of your LightRAG knowledge base — documents, processing status, and top entities.

## How it works

Hits multiple LightRAG API endpoints and presents a consolidated status report.

## Configuration

- **LightRAG server:** `http://localhost:9621` (default)

## Usage

Run these three requests and combine the results:

### 1. Check if documents are currently being processed

```bash
curl -s http://localhost:9621/documents/pipeline_status
```

Key fields:
- `busy` — `true` if processing is in progress
- `latest_message` — what's happening right now
- `docs` — documents in current batch

### 2. Get all documents and their status

```bash
curl -s http://localhost:9621/documents
```

Returns documents grouped by status: PENDING, PROCESSING, PROCESSED, FAILED.

### 3. Get the most connected entities (the hubs of the knowledge graph)

```bash
curl -s "http://localhost:9621/graph/label/popular?limit=15"
```

Returns the top entities sorted by how many connections they have — these are the central concepts in the knowledge base.

### Format the Output

Present a status report like:

```
LightRAG Knowledge Base Status
==============================
Server: http://localhost:9621 — Online
Processing: Idle (or "Processing 3 documents...")

Documents:
  Processed: 10
  Pending: 0
  Failed: 0

Top Entities (most connected):
  1. Anthropic (hub)
  2. Claude Code (hub)
  3. OpenAI (hub)
  4. LightRAG (hub)
  5. Model Context Protocol (hub)
  ...
```

### Error Handling

- If the server is unreachable: "LightRAG server is not responding at localhost:9621. Check that Docker is running: `docker ps`"
- If no documents exist: "Knowledge base is empty. Upload documents with /lightrag-upload"
