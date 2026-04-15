---
name: lightrag-explore
description: Explore entities and relationships in a LightRAG knowledge graph. Use this skill whenever the user wants to know what their knowledge base contains about a topic, explore connections in their knowledge graph, see what entities exist, or understand how concepts relate to each other. Triggers on phrases like "what does my KB know about", "explore the graph for", "show me connections to", "what entities relate to", or any request to browse or inspect the knowledge graph.
---

# LightRAG Explore

Explore your LightRAG knowledge graph — search for entities, view their connections, and understand how concepts relate to each other.

## How it works

Uses the LightRAG graph API endpoints to search for entities and retrieve subgraphs showing their relationships.

## Configuration

- **LightRAG server:** `http://localhost:9621` (default)

## Usage

### Step 1: Search for entities matching the user's topic

```bash
curl -s "http://localhost:9621/graph/label/search?q=SEARCH_TERM&limit=10"
```

Returns a JSON array of entity names that match the search term (fuzzy matching).

### Step 2: Get the subgraph around a specific entity

```bash
curl -s "http://localhost:9621/graphs?label=ENTITY_NAME&max_depth=2&max_nodes=30"
```

Parameters:
- `label` — the entity name to center the graph on
- `max_depth` — how many relationship hops to traverse (default: 2)
- `max_nodes` — maximum nodes to return (default: 30)

Returns JSON with:
- `nodes` — array of entities (each has `id`, `description`, etc.)
- `edges` — array of relationships (each has `source`, `target`, `description`)

### Step 3: Format the output

Present the results to the user as:

1. **Entity found:** [name]
2. **Connected to:** list of related entities with relationship descriptions
3. **Key relationships:** the most interesting connections

### Other Useful Endpoints

**List all entity labels:**
```bash
curl -s "http://localhost:9621/graph/label/list"
```

**Get most connected entities (hubs):**
```bash
curl -s "http://localhost:9621/graph/label/popular?limit=20"
```

**Check if a specific entity exists:**
```bash
curl -s "http://localhost:9621/graph/entity/exists?name=ENTITY_NAME"
```

### Example Flow

User: "What does my knowledge base know about MCP?"

1. Search: `curl -s "http://localhost:9621/graph/label/search?q=MCP&limit=10"`
   → Returns: ["Model Context Protocol (MCP)", "MCP Server", "MCP Servers"]

2. Get subgraph: `curl -s "http://localhost:9621/graphs?label=Model+Context+Protocol+(MCP)&max_depth=2&max_nodes=20"`
   → Returns nodes and edges

3. Format and present:
   > **Model Context Protocol (MCP)** is connected to:
   > - Claude Code (has deep MCP integration)
   > - Anthropic (introduced MCP in late 2024)
   > - Claude Desktop (MCP-compatible client)
   > - Databases, APIs, File Systems (connected via MCP servers)
   > ...

### Error Handling

- If no entities match the search, suggest broader search terms
- If the graph is empty, the knowledge base may not have been populated yet
