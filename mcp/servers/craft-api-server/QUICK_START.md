# Craft API MCP Server - Quick Start (5 Minutes)

## Step 1: Install Dependencies (2 min)

```bash
cd ~/mcp-servers/craft-api-server
npm install
```

## Step 2: Build the Server (1 min)

```bash
npm run build
```

You should see no errors. Check:
```bash
ls build/index.js
```

## Step 3: Test Run (1 min)

```bash
npm start
```

You should see: `Craft API MCP Server running on stdio`

Press `Ctrl+C` to stop.

## Step 4: Configure Your MCP Client (1 min)

### Option A: Claude Desktop

1. Find your config file:
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

2. Add this configuration:
```json
{
  "mcpServers": {
    "craft-api": {
      "command": "node",
      "args": ["/FULL/PATH/TO/craft-api-mcp-server/build/index.js"]
    }
  }
}
```

3. Restart Claude Desktop

### Option B: Terminal Testing

In one terminal, start the server:
```bash
npm start
```

In another terminal, test with your MCP client.

## Ready to Use!

Your MCP server is now ready. Use these tools:

| Tool | What it does |
|------|-------------|
| `list_documents` | See all Craft documents |
| `get_blocks` | Read document content |
| `insert_blocks` | Add content |
| `update_blocks` | Edit content |
| `delete_blocks` | Remove content |
| `search_documents` | Find content across docs |
| `list_collections` | See collections |
| `add_collection_items` | Add collection items |

## First Test

Ask Claude (with MCP enabled):
> "List all my Craft documents"

It should call the `list_documents` tool and show your documents.

## Common Issues

**Server won't start**
```bash
# Check Node.js version
node --version  # Should be 18+

# Rebuild
npm run build
npm start
```

**Permission denied**
```bash
chmod +x build/index.js
```

**Can't find config file**
- Create it if it doesn't exist
- Restart Claude Desktop after editing
- Verify path has no spaces or special characters

## Next Steps

1. Read **EXAMPLES.md** for usage patterns
2. Check **SETUP.md** for detailed configuration
3. See **ARCHITECTURE.md** for how it works

## Getting Help

- MCP documentation: https://modelcontextprotocol.io
- Craft API docs: https://connect.craft.do
- Check README.md for full reference

---

That's it! You're ready to use Craft API with your MCP client. 🚀
