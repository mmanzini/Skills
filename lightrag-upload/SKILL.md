---
name: lightrag-upload
description: Upload a document to a LightRAG knowledge base for indexing. Use this skill whenever the user wants to add a file to their knowledge base, index a document in LightRAG, or ingest new content into their knowledge graph. Triggers on phrases like "upload to lightrag", "add this to my knowledge base", "index this document", "ingest this file", or any request to add documents to a LightRAG instance.
---

# LightRAG Upload

Upload a document to your LightRAG knowledge base via the REST API for indexing into the knowledge graph.

## How it works

Send the file to the LightRAG server's `/upload` endpoint. LightRAG will process it in the background — extracting entities and relationships, building the knowledge graph, and creating vector embeddings.

## Configuration

- **LightRAG server:** `http://localhost:9621` (default)

## Usage

### Upload a file

```bash
curl -s -X POST http://localhost:9621/upload \
  -F "file=@/path/to/document.txt"
```

Supported file types: TXT, PDF, DOCX, PPTX, CSV, and other text-based formats.

### Check processing status

After uploading, check if the document is still being processed:

```bash
curl -s http://localhost:9621/documents/pipeline_status
```

Key fields in the response:
- `busy` — `true` if documents are still being processed
- `latest_message` — current processing step
- `docs` — number of documents in the current job

### Wait for completion

After uploading, poll the pipeline status every 5-10 seconds until `busy` is `false`. Then confirm to the user that the document has been indexed.

```bash
# Check status
curl -s http://localhost:9621/documents/pipeline_status | python -c "import sys,json; d=json.load(sys.stdin); print('Processing...' if d['busy'] else 'Done!'); print(d.get('latest_message',''))"
```

### Insert raw text (alternative)

If the user wants to index text directly (not a file):

```bash
curl -s -X POST http://localhost:9621/text \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"The text content to index here\"}"
```

### Example Flow

User: "Add my research notes to the knowledge base" (provides a file path)

1. Upload the file via `/upload`
2. Poll `/documents/pipeline_status` until `busy` is `false`
3. Confirm: "Document indexed. LightRAG extracted X entities and Y relationships."

### Error Handling

- If the server is unreachable, tell the user to check that Docker is running
- If upload fails, check that the file exists and is a supported format
- Large files may take several minutes to process — let the user know
