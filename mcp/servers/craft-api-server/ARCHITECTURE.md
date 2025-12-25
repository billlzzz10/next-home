# Craft API MCP Server - Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────┐
│            MCP Client (Claude, IDE, etc.)               │
└────────────────────────┬────────────────────────────────┘
                         │ MCP Protocol (JSON-RPC)
                         │
┌────────────────────────▼────────────────────────────────┐
│         Craft API MCP Server (Node.js/TypeScript)       │
├─────────────────────────────────────────────────────────┤
│  Request Handler Layer                                   │
│  ├─ ListToolsRequestSchema                              │
│  ├─ CallToolRequestSchema                               │
│  └─ Error Response Handling                             │
├─────────────────────────────────────────────────────────┤
│  Tool Implementation Layer                               │
│  ├─ Document Operations (list, get, insert, update)    │
│  ├─ Block Operations (CRUD, move)                       │
│  ├─ Search Operations (single/multi-document)           │
│  └─ Collection Operations (CRUD)                        │
├─────────────────────────────────────────────────────────┤
│  HTTP Client Layer (Axios)                              │
│  ├─ Request formatting                                  │
│  ├─ Error handling                                      │
│  └─ Timeout management                                  │
└────────────────────────┬────────────────────────────────┘
                         │ HTTPS
                         │
┌────────────────────────▼────────────────────────────────┐
│    Craft Multi-Document API (Remote)                    │
└─────────────────────────────────────────────────────────┘
```

## Components

### 1. CraftAPIServer Class

**Responsibility**: Main server orchestration

**Methods**:
- `setupTools()`: Define available tools and schemas
- `setupHandlers()`: Register MCP request handlers
- `handleToolCall()`: Route tool calls to implementations
- `run()`: Start the server on stdio transport

### 2. Request Handler Layer

**MCP Protocol Support**:
- `ListToolsRequestSchema`: Returns list of available tools
- `CallToolRequestSchema`: Executes tool calls

**Flow**:
```
Request → Validate → Route → Execute → Response
```

### 3. Tool Implementation Layer

#### Document Operations
- `listDocuments()`: GET /documents
- `getBlocks()`: GET /blocks
- `insertBlocks()`: POST /blocks
- `updateBlocks()`: PUT /blocks
- `deleteBlocks()`: DELETE /blocks

#### Block Organization
- `moveBlocks()`: PUT /blocks/move

#### Search Operations
- `searchDocument()`: GET /blocks/search (single document)
- `searchDocuments()`: GET /documents/search (multi-document)

#### Collection Operations
- `listCollections()`: GET /collections
- `getCollectionSchema()`: GET /collections/{id}/schema
- `getCollectionItems()`: GET /collections/{id}/items
- `addCollectionItems()`: POST /collections/{id}/items
- `deleteCollectionItems()`: DELETE /collections/{id}/items
- `updateCollectionItems()`: PUT /collections/{id}/items

### 4. HTTP Client Layer

**Axios Configuration**:
```typescript
{
  baseURL: "https://connect.craft.do/links/4hD3qTwgwc1/api/v1",
  timeout: 30000,
  headers: {
    "Content-Type": "application/json",
    "Accept": "application/json"
  }
}
```

**Error Handling**:
- Network errors → Descriptive error messages
- Timeout errors → Connection issues
- API errors → HTTP status codes

## Data Flow

### Write Operation Example: Insert Blocks

```
1. MCP Client sends request
   {
     "tool": "insert_blocks",
     "arguments": {
       "markdown": "...",
       "position": { "position": "end", "pageId": "doc-123" }
     }
   }

2. Server receives in CallToolRequestSchema handler

3. handleToolCall() routes to insertBlocks()

4. insertBlocks() validates arguments:
   - Check position exists
   - Check either markdown or blocks provided
   - Raise error if validation fails

5. Build HTTP request body:
   {
     "markdown": "...",
     "position": { "position": "end", "pageId": "doc-123" }
   }

6. Axios sends POST /blocks request to Craft API

7. Craft API processes and returns:
   {
     "items": [
       {
         "id": "block-123",
         "type": "text",
         "markdown": "..."
       }
     ]
   }

8. Server returns response to MCP Client
   {
     "content": [
       {
         "type": "text",
         "text": "{\"items\": [...]}"
       }
     ]
   }
```

### Read Operation Example: Search Documents

```
1. MCP Client sends request
   {
     "tool": "search_documents",
     "arguments": {
       "include": "project milestone",
       "documentIds": ["doc-123", "doc-456"]
     }
   }

2. Server validates arguments:
   - Ensure "include" parameter exists
   - Format optional parameters

3. Build query parameters:
   {
     "include": "project milestone",
     "documentIds": "doc-123,doc-456"
   }

4. Axios sends GET /documents/search with params

5. Craft API returns matching blocks with relevance:
   {
     "items": [
       {
         "documentId": "doc-123",
         "markdown": "The **project milestone** is scheduled..."
       }
     ]
   }

6. Response sent to MCP Client
```

## Error Handling Strategy

### Input Validation

All tool calls validate:
1. Required parameters present
2. Parameter types correct
3. Array/object structure valid

Example:
```typescript
if (!id) {
  throw new Error("id parameter is required");
}
```

### HTTP Error Handling

```typescript
try {
  const response = await this.client.post("/blocks", body);
  return response.data;
} catch (error) {
  // Axios error details included automatically
  throw new Error(`API Error: ${error.message}`);
}
```

### Response Transformation

Server returns standardized MCP response:
```typescript
{
  content: [
    {
      type: "text",
      text: JSON.stringify(result, null, 2),
      isError?: boolean
    }
  ]
}
```

## Tool Definition Schema

Each tool defines:

1. **name**: Unique identifier
2. **description**: Human-readable purpose
3. **inputSchema**: JSON Schema for parameters
   - type: "object"
   - properties: Parameter definitions
   - required: Required parameters

Example:
```typescript
{
  name: "get_blocks",
  description: "Fetch content from documents...",
  inputSchema: {
    type: "object",
    properties: {
      id: {
        type: "string",
        description: "The block ID to fetch"
      },
      maxDepth: {
        type: "number",
        description: "Maximum nesting depth"
      }
    },
    required: ["id"]
  }
}
```

## Transport Layer

### Stdio Transport

```
MCP Protocol Messages
    ↓
Node.js stdin/stdout
    ↓
JSON-RPC 2.0 Messages
```

**Message Format**:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "list_documents",
    "arguments": {}
  }
}
```

## Performance Considerations

### Timeout

- Default: 30 seconds
- Adjust in axios client for long-running operations
- Prevents indefinite hanging

### Pagination

For large results:
- Use `maxDepth` to limit nested content
- Implement client-side pagination logic
- Consider caching for repeated queries

### Rate Limiting

- No built-in rate limiting (respect Craft API limits)
- Implement in production if needed
- Consider exponential backoff for retries

## Security Model

### API Endpoint

- Hardcoded URL (single connection)
- No API key in request headers
- Access controlled by Craft connection URL

### Data Handling

- All data passed through JSON
- No encryption in transport (HTTPS handles this)
- No sensitive data logging

### Safe Operations

✅ **Safe**: GET requests, test creates/updates/deletes that are reversed
⚠️ **Risky**: Permanent deletes, production updates
❌ **Unsafe**: Unverified bulk operations, irreversible changes

## Extensibility

### Adding New Tools

1. Define tool in `setupTools()`:
```typescript
{
  name: "new_tool",
  description: "...",
  inputSchema: { ... }
}
```

2. Add case in `handleToolCall()`:
```typescript
case "new_tool":
  return this.newToolMethod(args);
```

3. Implement method:
```typescript
private async newToolMethod(args: Record<string, unknown>): Promise<unknown> {
  // Implementation
}
```

### Modifying API Endpoint

1. Edit `src/index.ts` BASE_URL
2. Rebuild: `npm run build`
3. Restart server

### Custom Error Handling

Extend error handling in `handleToolCall()` catch block.

## Testing Strategy

### Unit Tests (Future)
- Tool parameter validation
- Error message formatting
- Request building

### Integration Tests (Future)
- API connectivity
- Tool execution
- Error scenarios

### Manual Testing
```bash
npm start  # Start server
# Then use MCP client to test each tool
```

## Dependencies

### Production
- `@modelcontextprotocol/sdk`: MCP protocol implementation
- `axios`: HTTP client for API calls

### Development
- `typescript`: Type safety
- `@types/node`: Node.js type definitions

## Build Process

```
TypeScript Source (src/index.ts)
    ↓ (tsc compiler)
Compiled JavaScript (build/index.js)
    ↓ (npm start)
Running Node.js Process
    ↓ (stdio)
MCP Client Communication
```

---

For implementation details, see src/index.ts
For deployment, see SETUP.md
For usage examples, see EXAMPLES.md
