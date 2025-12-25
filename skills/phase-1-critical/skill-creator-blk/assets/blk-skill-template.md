# BL1NK Skill Template

Template for creating a new BL1NK skill with all required sections.

```yaml
---
name: my-skill
description: |
  One-sentence description of what skill does.
  Include:
  - Primary use case
  - When to use this skill
  - Example trigger phrase
  
  Use this skill when: [primary trigger]
  Also useful for: [secondary uses]
license: Complete terms in LICENSE.txt
---

# My Skill Name

[One paragraph introducing the skill and its purpose]

## About This Skill

[2-3 paragraphs explaining what the skill does and when to use it]

### BL1NK Context

This skill fits into **[Phase 1-4]** of the BL1NK implementation approach.

**Related Skills**: [List similar or dependent skills]
**Integration Points**: [What external systems does it integrate with?]
**Team Size**: [1-2 developers recommended / Complex, 2-3 developers]

See `references/blk-examples.md` for similar patterns.

## How It Works

### Input Format

```json
{
  "parameter1": "description",
  "parameter2": "description"
}
```

### Output Format

```json
{
  "status": "success|error",
  "result": {...},
  "message": "optional error message"
}
```

### Process

[Explain the step-by-step process]

## Bundled Resources

### Scripts (`scripts/`)
- `run.py` - Main implementation

### References (`references/`)
- `patterns.md` - Common usage patterns

### Assets (`assets/`)
- `template.txt` - Example template

## Testing

### Test 1: Basic Operation
**Input:**
```json
{"parameter": "value"}
```
**Expected Output:**
```json
{"status": "success", "result": {...}}
```

### Test 2: Error Handling
**Input:**
```json
{"parameter": ""}
```
**Expected Output:**
```json
{"status": "error", "message": "..."}
```

## Integration with BL1NK

### For Notifications
Import from `/home/user/projects/bl1nk-architect/src/notifications/notification_manager.py`:
- NotificationManager
- SlackNotifier
- LinearNotifier
- ClickUpNotifier

### For GitHub Integration
Import from `/home/user/projects/bl1nk-architect/src/github_client.py`:
- GithubClient

### For POE Protocol
Reference `/home/user/docs/poe-protocol/`:
- POE_PROTOCOL_SPEC.md
- QUICK_REFERENCE.md

### For Skill Orchestration
Import from `/home/user/projects/bl1nk-architect/src/skill_loader.py`:
- SkillLoader

## Manifest Registration

Update `/home/user/skills/manifest.json`:

```json
{
  "name": "my-skill",
  "title": "My Skill",
  "description": "Short description",
  "author": "BL1NK Team",
  "version": "1.0.0",
  "tags": ["tag1", "tag2"],
  "category": "category",
  "complexity": "low|medium|high",
  "estimated_runtime": 30
}
```

Update `/home/user/skills/skills.json`:

```json
{
  "id": "my-skill",
  "name": "My Skill",
  "description": "Short description",
  "version": "1.0.0",
  "language": "python"
}
```

## Usage Examples

### Example 1: [Use Case 1]
[Show real usage example]

### Example 2: [Use Case 2]
[Show real usage example]

## See Also

- `references/blk-examples.md` - Examples of similar skills
- `references/blk-patterns.md` - Common implementation patterns
- `references/phase-implementation.md` - Phase placement guide

## Troubleshooting

**Issue**: [Common problem]
**Solution**: [How to fix it]

## Notes

- [Important consideration 1]
- [Important consideration 2]

```

---

## Using This Template

1. Copy this template to your SKILL.md
2. Fill in all [bracketed] sections
3. Implement scripts/ directory
4. Create references/ docs
5. Add assets/ if needed
6. Run validation: `scripts/validate_blk_skill.py`
7. Package: `scripts/package_skill.py`

