# Craft API MCP Server - Setup Guide

## Prerequisites

- Node.js 18+ with npm
- Access to Craft multi-document connection
- MCP client (e.g., Claude Desktop, compatible IDE, etc.)

## Installation Steps

### 1. Clone/Download the Server

```bash
git clone <repository-url> craft-api-mcp-server
cd craft-api-mcp-server
```

Or download and extract the archive.

### 2. Install Dependencies

```bash
npm install
```

### 3. Build the TypeScript

```bash
npm run build
```

This creates the `build/` directory with compiled JavaScript.

### 4. Verify the Build

```bash
ls -la build/index.js
```

## Integration with MCP Clients

### Claude Desktop

Add this to your Claude Desktop configuration file (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS or `%APPDATA%\Claude\claude_desktop_config.json` on Windows):

```json
{
  "mcpServers": {
    "craft-api": {
      "command": "node",
      "args": ["/absolute/path/to/craft-api-mcp-server/build/index.js"],
      "env": {}
    }
  }
}
```

Replace `/absolute/path/to/craft-api-mcp-server` with the actual path.

### Running Standalone

```bash
npm start
```

The server will listen on stdin/stdout and wait for MCP protocol messages.

## Testing the Connection

### 1. Start the Server
```bash
npm start
```

### 2. Test with a Simple Query

You can test using the MCP CLI or any MCP-compatible client:

```bash
# List available tools
mcp craft-api
```

### 3. Call a Tool

```bash
mcp craft-api list_documents
```

## Troubleshooting

### Build Fails
```bash
# Clean and rebuild
rm -rf build/
npm install
npm run build
```

### Server Won't Start
```bash
# Check Node.js version
node --version  # Should be 18+

# Check dependencies
npm list

# Verify build output
ls -la build/
```

### API Errors

**403 Forbidden**
- Verify the API endpoint is correct
- Check if you have access to the Craft connection
- Verify the endpoint URL: https://connect.craft.do/links/4hD3qTwgwc1/api/v1

**Connection Timeout**
- Increase timeout in `src/index.ts` if needed
- Check network connectivity
- Verify Craft API server is running

**404 Not Found**
- Verify document/collection IDs are correct
- Use `list_documents` first to get valid IDs

## Configuration

### Changing the API Endpoint

Edit `src/index.ts` and modify:

```typescript
const BASE_URL = "https://your-craft-api-endpoint/api/v1";
```

Then rebuild:
```bash
npm run build
```

### Adjusting Timeout

In `src/index.ts`, modify the axios client creation:

```typescript
timeout: 60000,  // 60 seconds instead of 30
```

## Development

### Watch Mode
```bash
npm run watch
```

This will recompile TypeScript as you make changes.

### Development Build
```bash
npm run dev
```

Combines building and running in one command.

## Next Steps

1. Test with `list_documents` to verify connectivity
2. Explore document structure with `get_blocks`
3. Create test content with `insert_blocks`
4. Integrate with your MCP client

## Support

- For MCP documentation: https://modelcontextprotocol.io
- For Craft API docs: https://connect.craft.do
- Check logs for detailed error messages

## Security Notes

⚠️ **Important**: This server has direct access to your Craft documents. Be cautious with:
- DELETE operations (permanent)
- MOVE operations (can reorganize content)
- UPDATE operations (modifies content)

Always test with non-critical content first.

## Advanced Configuration

### Custom Logging

Edit `src/index.ts` to add detailed logging:

```typescript
private log(message: string, data?: unknown): void {
  console.error(JSON.stringify({ timestamp: new Date(), message, data }));
}
```

### Rate Limiting

Add request throttling for high-volume operations in `src/index.ts`.

### Caching

Implement Redis or in-memory caching for frequently accessed documents.

---

For more help, see README.md or check the Craft API documentation.
