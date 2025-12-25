# BL1NK Monorepo

AI-powered skill-based automation platform with modular architecture.

## Quick Start

```bash
make setup      # Install & configure
make build      # Build all packages
make test       # Run tests
```

## Project Structure

### 🎨 Core Applications (`apps/`)
- **web-portal** - Frontend user interface
- **api-server** - Backend REST API
- **cli-tool** - Command-line interface
- **obsidian-plugin** - Obsidian.md integration

### 📦 Shared Libraries (`packages/`)
- **core** - Business logic
- **ui** - Reusable UI components
- **auth** - Authentication utilities
- **integrations** - External service clients (GitHub, Slack, Linear, ClickUp, POE)
- **utils** - Common utilities

### 🎯 Skills (`skills/`)
Organized by implementation phase:

- **phase-1-critical/** (Week 1, 5-8h)
  - text-processor - Text analysis & transformation
  - log-analyzer - Log parsing & analysis
  - notification-router - Multi-channel notifications

- **phase-2-integration/** (Week 2, 9-12h)
  - github-repo-analyzer - GitHub repository health
  - prompt-optimizer - LLM prompt optimization
  - poe-bot-generator - POE protocol bot scaffolding

- **phase-3-platform/** (Week 3-4, 10-13h)
  - code-analyzer - Code quality analysis
  - skill-chain-executor - Multi-skill orchestration
  - document-generator - Auto documentation

- **phase-4-advanced/** (Backlog)
  - test-generator - Automated test generation

- **skill-creator-blk/** - BL1NK skill creation helper
- **manifest/** - Centralized skill registry

### 🔌 MCP Servers (`mcp/`)
- **servers/** - Individual MCP implementations
- **registry/** - Server registry & discovery

### 📚 Documentation (`docs/`)
- **architecture/** - System design & architecture
- **guides/** - How-to & tutorial documentation
- **api/** - API specifications
- **reference/** - Technical reference materials
- **analysis/** - Data analysis & reports
- **agents/** - AI system prompts

### 🧪 Tests (`tests/`)
- **unit/** - Unit tests
- **integration/** - Integration tests
- **e2e/** - End-to-end tests
- **fixtures/** - Test data & fixtures

### 🔧 Tools & Configuration
- **tools/** - Build scripts, Docker, CI/CD
- **config/** - Shared configuration files
- **.config/** - Workspace meta-configuration (hidden)
- **.local/** - Local development files (hidden, git-ignored)

### 📦 Archive (`archive/`)
- Historical files, deprecated skills, legacy documentation

## Development Commands

```bash
# Setup & Installation
make setup              # Full environment setup
make install            # Install dependencies only

# Development
make dev                # Run all services
make dev-api            # Run API server
make dev-web            # Run web portal
make dev-cli            # Run CLI tool

# Building
make build              # Build all packages
make build-api          # Build API
make build-web          # Build web UI

# Testing
make test               # Run all tests
make test-unit          # Unit tests only
make test-integration   # Integration tests only

# Quality
make lint               # Lint all code
make format             # Format code
make validate           # Validate monorepo structure

# Skills
make new-skill PHASE=1 NAME=my-skill  # Create new skill
make list-skills                       # List all skills by phase

# Deployment
make deploy             # Deploy to production
make deploy-api         # Deploy API only
make deploy-web         # Deploy web only
```

## Documentation

- [Getting Started](docs/guides/getting-started.md)
- [Architecture Overview](docs/architecture/monorepo.md)
- [Development Guide](docs/guides/development.md)
- [Skill Creation](docs/guides/skill-creation.md)
- [API Documentation](docs/api/README.md)

## Project Information

- **Language**: TypeScript, Python
- **Package Manager**: pnpm
- **License**: MIT
- **Status**: Active Development

## Contributing

See [CONTRIBUTING.md](docs/guides/CONTRIBUTING.md) for guidelines.

## Support

For questions or issues, please refer to the [FAQ](docs/reference/FAQ.md) or open an issue on GitHub.

---

**BL1NK** - Making AI automation modular and accessible.
