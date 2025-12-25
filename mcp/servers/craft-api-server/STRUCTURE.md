# Project Structure

```
craft-api-mcp-server/
│
├── 📋 Configuration & Metadata
│   ├── package.json              # npm dependencies and scripts
│   ├── tsconfig.json             # TypeScript configuration
│   ├── .env.example              # Environment variables template
│   ├── .gitignore                # Git ignore patterns
│   └── LICENSE                   # MIT License
│
├── 📚 Documentation (Read These!)
│   ├── PROJECT_SUMMARY.md        # ⭐ Overview of everything
│   ├── QUICK_START.md            # ⭐ 5-minute setup guide
│   ├── README.md                 # Complete reference manual
│   ├── SETUP.md                  # Detailed installation guide
│   ├── EXAMPLES.md               # 20+ real usage examples
│   ├── ARCHITECTURE.md           # System design & flow
│   └── STRUCTURE.md              # This file
│
├── 📁 Source Code
│   └── src/
│       └── index.ts              # Main MCP server (550+ lines, TypeScript)
│
├── 📁 Build Output (Auto-generated)
│   └── build/
│       ├── index.js              # Compiled JavaScript
│       ├── index.d.ts            # TypeScript declarations
│       └── index.js.map          # Source map for debugging
│
└── 📁 Node Modules (Auto-created)
    └── node_modules/             # Installed dependencies (after npm install)
```

## File Descriptions

### Configuration Files

| File | Purpose | Action |
|------|---------|--------|
| `package.json` | npm dependencies, scripts, metadata | Edit to add more dependencies |
| `tsconfig.json` | TypeScript compiler options | Modify for different TypeScript settings |
| `.env.example` | Template for environment variables | Copy to `.env` for your settings |
| `.gitignore` | Git ignore patterns | Standard Git config |
| `LICENSE` | MIT License | Legal stuff - don't modify |

### Documentation Files

| File | Best For | Read Time |
|------|----------|-----------|
| **PROJECT_SUMMARY.md** | Understanding what you have | 5 min |
| **QUICK_START.md** | Getting running immediately | 5 min |
| **README.md** | Complete API reference | 20 min |
| **SETUP.md** | Installation & configuration | 15 min |
| **EXAMPLES.md** | Real usage patterns | 20 min |
| **ARCHITECTURE.md** | How it works internally | 15 min |

### Source Code

```
src/index.ts (550+ lines)
│
├── Imports & Types
│   ├── MCP SDK imports
│   ├── Axios HTTP client
│   └── Custom interfaces
│
├── Constants
│   └── BASE_URL = "https://connect.craft.do/links/4hD3qTwgwc1/api/v1"
│
└── CraftAPIServer Class (main)
    ├── constructor()              # Initialize server & HTTP client
    ├── setupTools()               # Define 14 tools
    ├── setupHandlers()            # Register MCP handlers
    ├── handleToolCall()           # Route tool calls
    │
    ├── Document Operations
    │   ├── listDocuments()
    │   ├── getBlocks()
    │   ├── insertBlocks()
    │   ├── updateBlocks()
    │   └── deleteBlocks()
    │
    ├── Block Organization
    │   └── moveBlocks()
    │
    ├── Search Operations
    │   ├── searchDocument()       # Single document regex search
    │   └── searchDocuments()      # Multi-document relevance search
    │
    ├── Collection Operations
    │   ├── listCollections()
    │   ├── getCollectionSchema()
    │   ├── getCollectionItems()
    │   ├── addCollectionItems()
    │   ├── updateCollectionItems()
    │   └── deleteCollectionItems()
    │
    └── run()                      # Start server
```

## Getting Started with Each File

### 1. Start Here 👈
```bash
# Read overview
cat PROJECT_SUMMARY.md

# Then quick start
cat QUICK_START.md
```

### 2. Installation
```bash
# Read setup details
cat SETUP.md

# Then run
npm install
npm run build
```

### 3. Learn by Example
```bash
# See what you can do
cat EXAMPLES.md

# Use these examples with your MCP client
```

### 4. Understand How It Works
```bash
# Read architecture
cat ARCHITECTURE.md

# Review source code
cat src/index.ts
```

### 5. Reference Everything
```bash
# Complete API docs
cat README.md
```

## Command Reference

### Development Commands

```bash
# Install dependencies
npm install

# Build TypeScript → JavaScript
npm run build

# Watch for changes (auto-rebuild)
npm run watch

# Start the server
npm start

# Build and start together
npm run dev
```

### File Viewing Commands

```bash
# Quick overview
cat PROJECT_SUMMARY.md

# Fast setup
cat QUICK_START.md

# See all available tools
grep -A 5 "name:" src/index.ts | head -60

# Check TypeScript types
grep "interface" src/index.ts

# View available tools JSON
cat README.md | grep "^#### \`" | head -20
```

## File Sizes

```
📄 Source Code
   src/index.ts                    ~550 lines
   
📚 Documentation
   PROJECT_SUMMARY.md             ~200 lines
   QUICK_START.md                 ~100 lines
   README.md                      ~500 lines
   SETUP.md                       ~200 lines
   EXAMPLES.md                    ~400 lines
   ARCHITECTURE.md                ~300 lines
   STRUCTURE.md                   This file

⚙️ Configuration
   package.json                   ~20 lines
   tsconfig.json                  ~20 lines
   LICENSE                        ~20 lines
```

## How to Navigate

### If You Want To...

| Goal | Start Here |
|------|-----------|
| Understand what this is | PROJECT_SUMMARY.md |
| Get running in 5 minutes | QUICK_START.md |
| Find a tool for a task | EXAMPLES.md |
| See all available tools | README.md |
| Understand the flow | ARCHITECTURE.md |
| See the code | src/index.ts |
| Deploy to production | SETUP.md |
| Configure for Claude | SETUP.md → Integration section |

### If You Get Stuck

| Problem | Where to Look |
|---------|---------------|
| Install won't work | SETUP.md → Troubleshooting |
| Don't know how to use it | EXAMPLES.md |
| Need tool reference | README.md → Tools Available |
| Want to know how it works | ARCHITECTURE.md |
| Getting API errors | README.md → Common Issues |

## Recommended Reading Order

### First Time
1. ⭐ PROJECT_SUMMARY.md (5 min)
2. ⭐ QUICK_START.md (5 min)
3. EXAMPLES.md (20 min)

### Setup & Configuration
4. SETUP.md (15 min)
5. Configure your MCP client

### Deep Dive
6. ARCHITECTURE.md (15 min)
7. src/index.ts (30 min)
8. README.md as reference

## File Dependencies

```
QUICK_START.md
    ↓
package.json → npm install
    ↓
tsconfig.json → npm run build
    ↓
src/index.ts (TypeScript)
    ↓ (compiled by tsc)
build/index.js (JavaScript)
    ↓
npm start
    ↓
MCP Server Running!
```

## Where to Make Changes

| Change Type | File | How |
|-------------|------|-----|
| Change API endpoint | src/index.ts | Edit `BASE_URL` constant |
| Add a new tool | src/index.ts | Follow pattern of existing tools |
| Adjust timeout | src/index.ts | Edit axios client config |
| Update docs | EXAMPLES.md or README.md | Just edit as needed |
| Add dependency | package.json | Edit dependencies section |
| Change TypeScript settings | tsconfig.json | Modify compiler options |

## Build Process Flow

```
Human writes TypeScript
       ↓
src/index.ts
       ↓ (npm run build)
tsc compiler
       ↓
JavaScript compiled
       ↓
build/index.js
       ↓ (npm start)
Node.js runtime
       ↓
MCP Server on stdio
       ↓
MCP Client (Claude)
```

## Quick Reference

### View All Tools
```bash
grep '"name": "' src/index.ts | sed 's/.*"name": "\([^"]*\)".*/\1/'
```

### See Tool Count
```bash
grep '"name": "' src/index.ts | wc -l
```

### Check Build Status
```bash
ls -lh build/index.js
```

### View Recent Changes
```bash
git log --oneline (if in git)
```

## Summary

- **10 documentation files** for different needs
- **1 main source file** with all 14 tools
- **Configuration files** for build & deployment
- **Clear directory structure** for easy navigation

Start with **QUICK_START.md** and go from there!

---

For the complete visual map, see PROJECT_SUMMARY.md
