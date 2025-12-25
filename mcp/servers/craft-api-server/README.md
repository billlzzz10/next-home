# Craft API MCP Server

A Model Context Protocol (MCP) server that provides comprehensive access to the Craft Multi-Document API. This server bridges Claude and other MCP-compatible clients with Craft's document management capabilities.

## Features

✨ **Complete API Coverage**
- Document management (list, fetch, create, update, delete)
- Block operations (CRUD, move, reorder)
- Multi-document search with relevance ranking
- Collection management (CRUD operations)
- Full markdown content support

🔐 **Production Ready**
- Proper error handling and validation
- Timeout protection (30s default)
- TypeScript for type safety
- Comprehensive logging

## Quick Start

### Installation

```bash
cd ~/mcp-servers/craft-api-server
npm install
npm run build
```

### Running the Server

```bash
npm start
```

The server will start on stdio transport.

## Tools Available

### Document Operations

#### `list_documents`
Retrieve all documents accessible through the multi-document connection.

**Parameters:** None

**Example:**
```json
{
  "result": {
    "items": [
      {"id": "doc-123", "title": "Project Plan", "isDeleted": false}
    ]
  }
}
```

#### `get_blocks`
Fetch content from documents with nested children.

**Parameters:**
- `id` (required): Document/page/block ID
- `maxDepth` (optional): Maximum depth (-1 = all, 0 = block only, 1 = direct children)
- `fetchMetadata` (optional): Include metadata (comments, timestamps, etc.)

**Example:**
```json
{
  "id": "doc-123",
  "maxDepth": 2,
  "fetchMetadata": true
}
```

#### `insert_blocks`
Insert content into documents.

**Parameters:**
- `markdown` or `blocks` (required): Content to insert
- `position` (required): Where to insert
  - `position`: "start", "end", "before", "after"
  - `pageId`: Target document ID
  - `targetBlockId`: For before/after positioning

**Example:**
```json
{
  "markdown": "## New Section\n\n- Point A\n- Point B",
  "position": {
    "position": "end",
    "pageId": "doc-123"
  }
}
```

#### `update_blocks`
Update content across documents.

**Parameters:**
- `blocks` (required): Array of blocks with id and fields to update

**Example:**
```json
{
  "blocks": [
    {
      "id": "5",
      "markdown": "## Updated Section\n\nUpdated content"
    }
  ]
}
```

#### `delete_blocks`
Delete content from documents.

**Parameters:**
- `blockIds` (required): Array of block IDs to delete

#### `move_blocks`
Move blocks to reorder or move between documents.

**Parameters:**
- `blockIds` (required): Array of block IDs to move
- `position` (required): Target position

### Search Operations

#### `search_document`
Search content within a single document using regex.

**Parameters:**
- `documentId` (required): Document to search
- `pattern` (required): Regular expression pattern
- `caseSensitive` (optional): Default false
- `beforeBlockCount` (optional): Context blocks before
- `afterBlockCount` (optional): Context blocks after

#### `search_documents`
Search across multiple documents with relevance ranking.

**Parameters:**
- `include` (required): Search terms
- `documentIds` (optional): Filter specific documents
- `documentFilterMode` (optional): "include" or "exclude"

### Collection Operations

#### `list_collections`
List all collections across documents.

**Parameters:**
- `documentIds` (optional): Filter by document

#### `get_collection_schema`
Get schema for a collection.

**Parameters:**
- `collectionId` (required): Collection ID
- `format` (optional): Schema format (default: json-schema-items)

#### `get_collection_items`
Retrieve all items from a collection.

**Parameters:**
- `collectionId` (required): Collection ID

#### `add_collection_items`
Add new items to a collection.

**Parameters:**
- `collectionId` (required): Collection ID
- `items` (required): Array of items with `title` and `properties`

#### `delete_collection_items`
Delete items from a collection.

**Parameters:**
- `collectionId` (required): Collection ID
- `idsToDelete` (required): Array of item IDs

#### `update_collection_items`
Update existing collection items.

**Parameters:**
- `collectionId` (required): Collection ID
- `itemsToUpdate` (required): Array of items with `id` field

## Configuration

### Base URL
The server is configured to use the Craft API endpoint:
```
https://connect.craft.do/links/4hD3qTwgwc1/api/v1
```

To change the API endpoint, modify the `BASE_URL` constant in `src/index.ts`.

### Timeout
Default timeout is 30 seconds. Adjust in the axios client creation if needed.

## Development

### Building
```bash
npm run build
```

### Watching for Changes
```bash
npm run watch
```

### Development Mode
```bash
npm run dev
```

## Architecture

- **TypeScript**: Full type safety
- **Axios**: HTTP client for API calls
- **MCP SDK**: Model Context Protocol implementation
- **Stdio Transport**: Standard input/output communication

## Error Handling

The server includes comprehensive error handling for:
- Missing required parameters
- API failures
- Network timeouts
- Invalid data formats

All errors are returned with descriptive messages.

## Security Considerations

⚠️ **Important**: This server connects to the actual Craft API. Be careful with:
- **DELETE operations**: Permanent data loss
- **UPDATE operations**: Verify changes are correct
- **MOVE operations**: Ensure proper positioning

Always test with non-critical data first.

## Limitations

- Single endpoint configuration (modify source to use different endpoints)
- No built-in caching
- No rate limiting (respect Craft API limits)
- 30-second timeout on all requests

## Support

For API documentation, visit: https://connect.craft.do

For MCP information: https://modelcontextprotocol.io

## License

MIT
