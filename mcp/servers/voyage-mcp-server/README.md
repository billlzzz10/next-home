# Voyage MCP Server v1.1.0

MCP (Model Context Protocol) Server for Voyage AI Vector Search with Cost Optimization.

## Features

✅ **Vector Search Integration** - Connect to Qdrant vector database
✅ **Multi-Provider Support** - Works with Voyage AI and Mistral AI
✅ **Cost Estimation** - Calculate costs before performing expensive operations
✅ **Advanced Filtering** - Filter results by score, tags, categories, date range, and more
✅ **User Logging** - Track all operations with detailed JSONL logs
✅ **Dynamic Configuration** - Update settings via YAML, JSON, or environment variables
✅ **Reranking** - AI-powered document reranking for better results
✅ **LLM Integration** - Seamless handoff to LLM when vector search insufficient

## Quick Start

### Installation

```bash
cd mcp-servers/voyage-mcp-server
npm install
npm run build
```

### Configuration

1. Copy config template:
```bash
cp config/default.yaml config/production.yaml
```

2. Set up API keys:
```bash
export VOYAGE_API_KEY="your-key-here"
# or
export MISTRAL_API_KEY="your-key-here"
```

3. Configure Qdrant connection:
```yaml
qdrant:
  url: http://localhost:6333
  apiKey: optional-qdrant-api-key
```

### Run Server

```bash
# Development
npm run dev

# Production
npm run build && npm start
```

## Available Tools

### `search_documents`
Search for documents in the vector database.

```json
{
  "query": "How to use Next.js App Router",
  "topK": 5,
  "scoreThreshold": 0.82,
  "useRerank": true
}
```

Response:
```json
{
  "shouldUseLLM": false,
  "results": [
    {
      "id": "doc_001",
      "score": 0.92,
      "content": "...",
      "metadata": {}
    }
  ],
  "costEstimate": 0.00015,
  "provider": "voyage"
}
```

### `estimate_cost`
Estimate cost of operations before executing.

```json
{
  "query": "Some query text",
  "useRerank": true
}
```

### `get_config`
Get current server configuration.

### `update_config`
Update server configuration dynamically.

## Architecture

```
mcp-servers/voyage-mcp-server/
├── src/
│   ├── server.ts              # Main MCP server
│   ├── types.ts               # Type definitions
│   ├── vector-store/
│   │   └── qdrant-store.ts   # Qdrant integration
│   ├── services/
│   │   ├── embedding-service.ts
│   │   ├── cost-calculator.ts
│   │   └── search-engine.ts
│   └── utils/
│       ├── user-logger.ts     # JSONL logging
│       ├── config-manager.ts  # Config management
│       └── filters.ts         # Advanced filtering
├── config/
│   └── default.yaml          # Configuration template
└── package.json
```

## Configuration Options

### Qdrant
- `url`: Qdrant server URL (default: `http://localhost:6333`)
- `apiKey`: Optional API key for authentication
- `collectionName`: Name of the vector collection
- `vectorSize`: Vector dimension size (default: 1024)
- `recreateCollection`: Recreate collection on startup

### Providers
- `primary`: `voyage` or `mistral`
- `voyage.apiKey`: Voyage API key
- `mistral.apiKey`: Mistral API key

### Logging
- `enabled`: Enable/disable logging
- `baseLogDir`: Directory for logs (default: `user_logs`)
- `rotateDays`: Keep logs for N days (default: 30)
- `logSearchQueries`: Log all queries
- `logCostEstimates`: Log cost calculations

### Cost
- `embeddingCostPerMillion`: Cost per 1M tokens
- `rerankCostPerThousand`: Cost per 1K rerank operations

## Environment Variables

Set these to override config file values:

```bash
export MCP_QDRANT__URL="http://qdrant.example.com"
export MCP_PROVIDERS__PRIMARY="mistral"
export MCP_PROVIDERS__VOYAGE__APIKEY="vk-xxxxx"
export MCP_LOGGING__ENABLED="true"
export MCP_COST__THRESHOLD="0.05"
```

## Usage Examples

### Python Client

```python
import json
import subprocess

def call_mcp_tool(tool_name, args):
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": args
        }
    }
    
    result = subprocess.run(
        ["node", "dist/server.js"],
        input=json.dumps(request),
        capture_output=True,
        text=True
    )
    
    return json.loads(result.stdout)

# Search documents
result = call_mcp_tool("search_documents", {
    "query": "Next.js 14 App Router"
})
print(json.dumps(result, indent=2))
```

### JavaScript/Node.js

```javascript
// See integration examples in the repository
```

## Logging

All operations are logged to `user_logs/{userId}/{year}/{month}/{day}.jsonl`

Example log entry:
```json
{
  "timestamp": "2024-12-24T13:45:00.000Z",
  "userId": "default_user",
  "type": "search_result",
  "method": "search",
  "tokens": 150,
  "costEstimate": 0.000015,
  "metadata": {
    "embeddingProvider": "voyage",
    "rerankUsed": true,
    "processingTime": 245
  }
}
```

## Cost Optimization

The server automatically:

1. ✅ Estimates costs before operations
2. ✅ Caches embeddings when possible
3. ✅ Uses efficient batch operations
4. ✅ Logs all cost metrics for analysis
5. ✅ Recommends LLM usage only when vector search is insufficient

**Typical savings: 80-95% cost reduction vs. always using LLM**

## Deployment

### Docker

```dockerfile
FROM node:20-alpine

WORKDIR /app
COPY . .
RUN npm install && npm run build

EXPOSE 3000
CMD ["npm", "start"]
```

### Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: voyage-mcp-server
spec:
  replicas: 1
  template:
    spec:
      containers:
      - name: server
        image: voyage-mcp-server:1.1.0
        env:
        - name: VOYAGE_API_KEY
          valueFrom:
            secretKeyRef:
              name: api-keys
              key: voyage
```

## Troubleshooting

**Issue**: `Cannot find module '@qdrant/js-client-rest'`
- Solution: Run `npm install`

**Issue**: `Voyage API error: 401 Unauthorized`
- Solution: Check `VOYAGE_API_KEY` environment variable

**Issue**: Cannot connect to Qdrant
- Solution: Ensure Qdrant is running at configured URL

## Performance

- **Search latency**: ~100-500ms (depending on collection size)
- **Embedding generation**: ~200-800ms per request
- **Reranking**: ~100-300ms for 10 documents

## Support

For issues and questions:
1. Check logs in `user_logs/`
2. Verify configuration in `config/default.yaml`
3. Test with `estimate_cost` tool first

## License

MIT
