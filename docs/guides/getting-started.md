# Getting Started with BL1NK Monorepo

## Prerequisites

- Node.js >= 18.0.0
- pnpm >= 8.0.0
- Git
- Python 3.8+ (for some skills)

## Installation

### 1. Clone Repository
```bash
git clone https://github.com/bl1nk/monorepo.git
cd bl1nk-monorepo
```

### 2. Setup Environment
```bash
make setup
```

This will:
- Create local directories (.local/cache, .credentials, etc.)
- Install all dependencies
- Setup git hooks

### 3. Verify Installation
```bash
make validate
```

You should see all checks pass.

## Development Workflow

### Running Services

```bash
# API Server
make dev-api        # Starts on http://localhost:3000

# Web Portal
make dev-web        # Starts on http://localhost:5173

# CLI Tool
make dev-cli        # Interactive command-line interface
```

### Building

```bash
# Build all packages
make build

# Build specific app
make build-api
make build-web
```

### Testing

```bash
# Run all tests
make test

# Unit tests only
make test-unit

# Integration tests
make test-integration
```

### Code Quality

```bash
# Lint all code
make lint

# Auto-format code
make format

# Check structure
make validate
```

## Creating Your First Skill

### 1. Create Skill Structure
```bash
make new-skill PHASE=1 NAME=my-skill
```

This creates:
```
skills/phase-1-critical/my-skill/
├── SKILL.md
├── scripts/
│   └── run.py
├── references/
└── assets/
```

### 2. Edit SKILL.md
```yaml
---
name: my-skill
description: My skill description
version: 1.0.0
author: Your Name
tags: [tag1, tag2]
---

# My Skill

Documentation here...
```

### 3. Implement run.py
```python
#!/usr/bin/env python3
import json
import sys

data = json.loads(sys.stdin.read())

# Your logic here
result = {"status": "success"}

print(json.dumps(result))
```

### 4. Test Skill
```bash
echo '{"param": "value"}' | python skills/phase-1-critical/my-skill/scripts/run.py
```

### 5. Validate
```bash
make validate
```

## Project Structure Guide

### I Want To...

#### Add a New Application
```bash
mkdir -p apps/my-app
cd apps/my-app
npm init -y
```

#### Add a Shared Library
```bash
mkdir -p packages/my-lib
cd packages/my-lib
npm init -y
```

#### Create a Skill
```bash
make new-skill PHASE=1 NAME=my-skill
```

#### List All Skills
```bash
make list-skills
```

#### Write Documentation
```bash
# Create in docs/
# - docs/guides/       (how-to guides)
# - docs/architecture/ (system design)
# - docs/api/          (API specs)
```

## Common Commands Quick Reference

```bash
make help           # Show all commands
make setup          # Initial setup
make install        # Install dependencies
make dev            # Run services
make dev-api        # API only
make dev-web        # Web only
make build          # Build all
make test           # Run tests
make lint           # Check code style
make format         # Auto-format code
make validate       # Verify structure
make clean          # Clean artifacts
```

## Troubleshooting

### Dependencies Won't Install
```bash
# Clear cache
rm -rf .local/cache
rm pnpm-lock.yaml

# Reinstall
make setup
```

### Port Already in Use
```bash
# Change port in app config or
make dev-api --port 3001
```

### Permission Denied on Scripts
```bash
chmod +x tools/scripts/*.sh
```

### Git Hooks Not Running
```bash
# Reinstall hooks
chmod +x .config/git/hooks/*
```

## Next Steps

1. **Explore Documentation** - Read docs/architecture/monorepo.md
2. **Run Services** - Try `make dev-api` and `make dev-web`
3. **Create First Skill** - Follow skill creation guide
4. **Read Guidelines** - Check docs/guides/development.md
5. **Join Community** - See CONTRIBUTING.md

## Resources

- [Architecture Overview](../architecture/monorepo.md)
- [Development Guide](development.md)
- [Skill Creation](skill-creation.md)
- [API Documentation](../api/README.md)

## Getting Help

- Check [FAQ](../reference/FAQ.md)
- Read [Troubleshooting](../reference/troubleshooting.md)
- Open an issue on GitHub

---

Welcome to BL1NK! 🚀
