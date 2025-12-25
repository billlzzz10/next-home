# Skills Manifest

This directory contains the central registry for all BL1NK skills.

## Files

- **manifest.json** - Complete skill metadata with detailed schema
- **skills.json** - Compact skill list for quick reference

## Organization

Skills are organized by implementation phase in the parent `skills/` directory:

- `phase-1-critical/` - Foundation skills (Week 1, 5-8h)
- `phase-2-integration/` - Integration skills (Week 2, 9-12h)
- `phase-3-platform/` - Platform skills (Week 3-4, 10-13h)
- `phase-4-advanced/` - Advanced skills (Backlog)

## Skill Structure

Each skill follows this format:

```
phase-N/
└── skill-name/
    ├── SKILL.md               # Metadata & documentation
    ├── scripts/
    │   └── run.py             # Implementation
    ├── references/            # Documentation
    └── assets/                # Templates
```

## Adding a New Skill

1. Create skill directory:
   ```bash
   make new-skill PHASE=1 NAME=my-skill
   ```

2. Implement in `scripts/run.py`

3. Update manifest files:
   ```json
   {
     "name": "my-skill",
     "phase": 1,
     "description": "...",
     "status": "active"
   }
   ```

4. Validate structure:
   ```bash
   make validate
   ```

