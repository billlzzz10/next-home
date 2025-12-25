# BL1NK Monorepo Architecture

## Overview

BL1NK follows a monorepo structure to manage multiple interconnected applications, libraries, and skills in a single repository.

## Directory Structure

```
bl1nk-monorepo/
├── apps/                   Core applications
├── packages/               Shared libraries & utilities
├── skills/                 Skills organized by phase
├── mcp/                    MCP server implementations
├── docs/                   Documentation
├── tests/                  Test infrastructure
├── tools/                  Build & deployment tools
├── config/                 Shared configuration
├── .config/                Workspace meta-config (hidden)
├── .local/                 Local dev files (hidden, git-ignored)
└── archive/                Historical & deprecated files
```

## Core Principles

### 1. Separation of Concerns
- **apps/** - User-facing applications
- **packages/** - Reusable, shared code
- **skills/** - Domain-specific capabilities
- **mcp/** - Protocol implementations

### 2. Phase-Based Organization
Skills are organized by implementation phase reflecting project timeline:
- Phase 1: Critical foundation (Week 1, 5-8h)
- Phase 2: Integration (Week 2, 9-12h)
- Phase 3: Platform maturity (Week 3-4, 10-13h)
- Phase 4: Advanced capabilities (Backlog)

### 3. Hidden Complexity
- **.config/** - Workspace configuration (Git-tracked)
- **.local/** - Local development files (Git-ignored)
- Keeps root clean with only 7 essential files

### 4. Centralized Documentation
All documentation in **docs/** organized by type:
- architecture/ - System design
- guides/ - How-to documentation
- api/ - API specifications
- reference/ - Technical reference
- analysis/ - Data analysis
- agents/ - System prompts

## File Organization

### Root Level (7 Essential Files)
- README.md - Project overview
- Makefile - Build automation
- package.json - Workspace config
- pnpm-workspace.yaml - Monorepo setup
- .gitignore - Git rules
- .editorconfig - Editor settings
- LICENSE - Project license

### Hidden Directories

#### .config/ (Git-Tracked)
Contains workspace meta-configuration:
```
.config/
├── git/           Git configuration & hooks
├── docker/        Docker templates
└── ci-cd/         CI/CD workflows
```

#### .local/ (Git-Ignored)
Contains local development artifacts:
```
.local/
├── cache/         Build & package cache
├── credentials/   Local API keys
└── temp/          Temporary files
```

## Development Workflow

```bash
# Setup environment
make setup

# Development
make dev-api      # Run API server
make dev-web      # Run web portal

# Build & Test
make build        # Build all packages
make test         # Run tests

# Quality
make lint         # Lint code
make format       # Format code
make validate     # Validate structure

# Skills
make new-skill PHASE=1 NAME=my-skill
```

## Workspace Strategy

### Version Control (.gitignore)

**Git-Ignored:**
- .local/ (local dev files)
- node_modules/ (dependencies)
- dist/, build/ (artifacts)
- *.log (logs)

**Tracked:**
- .config/ (workspace config)
- docs/ (documentation)
- skills/ (skill definitions)
- apps/ (applications)
- packages/ (libraries)

### Scalability

Adding new components:

**New App:**
```bash
mkdir -p apps/my-app
```

**New Package:**
```bash
mkdir -p packages/my-lib
```

**New Skill:**
```bash
make new-skill PHASE=1 NAME=my-skill
```

## Integration Points

### Package Dependencies
Packages can depend on each other through pnpm workspaces:
```json
{
  "dependencies": {
    "@bl1nk/core": "workspace:*",
    "@bl1nk/ui": "workspace:*"
  }
}
```

### Skill Dependencies
Skills can reference integration packages:
```python
from bl1nk.integrations.github import GithubClient
from bl1nk.integrations.slack import SlackNotifier
```

### MCP Integration
Skills can be exposed as MCP servers for external consumption.

## Best Practices

1. **Keep root clean** - Only essential files
2. **Use phase organization** - Easy to understand priority
3. **Centralize config** - Avoid duplication
4. **Hide complexity** - .config/ and .local/
5. **Document everything** - Centralized in docs/
6. **Version carefully** - Only track necessary files

## Migration from Flat Structure

When migrating from a flat structure:

1. Create monorepo directories
2. Move docs/ → docs/
3. Move projects/ → apps/
4. Move skills/ → skills/phase-*/
5. Move mcp-servers/ → mcp/servers/
6. Archive old root files → archive/
7. Update all import paths
8. Run `make validate` to verify

