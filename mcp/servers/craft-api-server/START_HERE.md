# 🚀 START HERE - Craft API MCP Server

Welcome! You have a fully functional MCP Server ready to connect Claude to Craft's API.

## ⏱️ 5-Minute Quick Start

```bash
# 1. Install (2 min)
cd ~/mcp-servers/craft-api-server
npm install

# 2. Build (1 min)
npm run build

# 3. Test (1 min)
npm start
# You should see: "Craft API MCP Server running on stdio"
# Press Ctrl+C to stop
```

**That's it!** Your server is ready. Now configure your MCP client.

## 🎯 What You Have

| Item | Count |
|------|-------|
| **Tools** | 14 production-ready tools |
| **Documentation** | 8 comprehensive guides |
| **Examples** | 20+ real-world use cases |
| **Setup Time** | 5 minutes |
| **Ready** | ✅ Production-ready |

## 📋 Next: Configure Your Client

### Claude Desktop (Recommended)

1. Find config file:
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

2. Add this (replace path):
```json
{
  "mcpServers": {
    "craft-api": {
      "command": "node",
      "args": ["/ABSOLUTE/PATH/TO/craft-api-mcp-server/build/index.js"]
    }
  }
}
```

3. Restart Claude Desktop

4. Test: Ask Claude "List my Craft documents"

## 📚 Documentation Map

| Need | File | Time |
|------|------|------|
| Overview | PROJECT_SUMMARY.md | 5 min |
| Setup help | QUICK_START.md | 5 min |
| How to use | EXAMPLES.md | 20 min |
| All tools | README.md | 20 min |
| Deep dive | ARCHITECTURE.md | 15 min |
| Navigation | INDEX.md | 5 min |

## 🛠️ 14 Available Tools

**Documents**: list, get, insert, update, delete, move
**Search**: search in one doc, search all docs
**Collections**: list, get schema, get items, add, update, delete items

## ✅ Checklist

- [ ] Installed npm packages (`npm install`)
- [ ] Built the server (`npm run build`)
- [ ] Tested it runs (`npm start`)
- [ ] Added to Claude Desktop config
- [ ] Restarted Claude Desktop
- [ ] Asked Claude to list your documents

## 🎓 Learning Path

1. **Now** → Run `npm install && npm run build && npm start`
2. **Next** → Read EXAMPLES.md (see what you can do)
3. **Then** → Try with Claude (ask it to list documents)
4. **Deep** → Read ARCHITECTURE.md (understand how it works)

## 💡 First Commands to Try

Ask Claude these with MCP enabled:

```
"List all my Craft documents"
→ Uses: list_documents tool

"Show me my Craft documents and their contents"
→ Uses: list_documents + get_blocks tools

"Search for 'project' in my Craft documents"
→ Uses: search_documents tool
```

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| `npm install` fails | Check Node.js 18+ with `node --version` |
| `npm run build` fails | Run `rm -rf node_modules` then `npm install` again |
| Can't find config file | Create it if it doesn't exist, restart Claude |
| Permission denied | Run `chmod +x build/index.js` |
| Claude doesn't see tools | Restart Claude Desktop completely |

## 📞 Need Help?

- **Setup issues?** → Read SETUP.md
- **Don't understand?** → Read EXAMPLES.md
- **Need reference?** → Read README.md
- **How it works?** → Read ARCHITECTURE.md
- **Everything else?** → Read INDEX.md

## 🎉 You're Ready!

Your Craft API MCP Server is:
- ✅ Installed
- ✅ Built
- ✅ Documented
- ✅ Ready to use

**Next step**: Configure your MCP client (see "Configure Your Client" above)

Then ask Claude: **"List my Craft documents"**

---

### Quick Links

| File | Purpose |
|------|---------|
| QUICK_START.md | Detailed 5-step guide |
| EXAMPLES.md | 20+ code examples |
| README.md | Complete API reference |
| ARCHITECTURE.md | System design |
| INDEX.md | Complete navigation |

### Commands Cheat Sheet

```bash
# Setup
npm install                    # Install dependencies
npm run build                  # Compile TypeScript
npm start                      # Run server
npm run watch                  # Auto-rebuild on changes
npm run dev                    # Build + run together

# Verify
ls build/index.js              # Check build exists
node --version                 # Check Node.js version
```

---

**Ready?** Start with:
```bash
npm install && npm run build && npm start
```

Then configure your MCP client and enjoy! 🚀
