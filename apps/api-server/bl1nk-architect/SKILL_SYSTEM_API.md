# Bl1nk Architect Skill System API

**Version**: 1.0 | **Status**: Production Ready

Enables Bl1nk Architect to load, manage, and execute Agent Skills as Poe script bots.

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [API Reference](#api-reference)
4. [Integration Guide](#integration-guide)
5. [Examples](#examples)
6. [Deployment](#deployment)

---

## Overview

The Skill System transforms Bl1nk Architect from a single-purpose analyzer into a **pluggable platform** that can:

✅ Load Agent Skills from filesystem
✅ Execute skills as Poe script bots
✅ Route queries to appropriate skills
✅ Chain multiple skills together
✅ Expose skill directory via API
✅ Support dynamic bot creation per skill

### Key Components

| Component | Purpose | Location |
|-----------|---------|----------|
| **SkillLoader** | Discover and load skills | `src/skill_loader.py` |
| **SkillRegistry** | Manage loaded skills | `src/skill_loader.py` |
| **PoeSkillRouter** | Route queries to skills | `src/poe_plugin_manager.py` |
| **PoeSkillBot** | Execute skills in Poe | `src/poe_plugin_manager.py` |
| **DynamicSkillBot** | Individual bot per skill | `src/poe_plugin_manager.py` |
| **Bl1nkWithSkills** | Enhanced analyzer | `src/bot_with_skills.py` |

---

## Architecture

### Skill Discovery & Loading

```
Filesystem
  ├── /home/user/skills/
  │   ├── skill-1/
  │   │   ├── SKILL.md (with YAML frontmatter)
  │   │   ├── scripts/
  │   │   │   └── *.py
  │   │   └── resources/
  │   │       └── *.*
  │   └── skill-2/
  │       └── SKILL.md
  │
  ↓
SkillDiscovery
  ├── find_skills() → List[Path]
  ├── parse_skill_file() → SkillContent
  └── _find_scripts() → Dict[str, str]
  
  ↓
SkillRegistry
  ├── register(skill)
  ├── get_skill(id)
  ├── list_skills()
  └── find_skills_by_tag()
  
  ↓
SkillLoader
  ├── load_all_skills()
  ├── load_skill(path)
  └── get_bot(id)
```

### Query Routing

```
User Query (Poe)
    ↓
Bl1nkArchitectWithSkillsBot.get_response()
    ├─ Check if skill command?
    │  ├─ Yes → PoeSkillRouter
    │  └─ No → Continue
    │
    ├─ Should use skill?
    │  ├─ Yes → Route to SkillBot
    │  └─ No → Original Analyzer
    │
    ↓
Execute & Return Result
```

---

## API Reference

### SkillLoader

```python
from src.skill_loader import get_skill_loader

loader = get_skill_loader()
```

#### `load_all_skills() → int`
Discover and load all skills from filesystem.

```python
count = loader.load_all_skills()
# Returns: Number of skills loaded
```

#### `load_skill(skill_path: str) → Optional[SkillBot]`
Load a specific skill by path.

```python
bot = loader.load_skill("/path/to/skill")
if bot:
    result = await bot.call_with_instructions(query)
```

#### `get_bot(skill_id: str) → Optional[SkillBot]`
Get loaded bot by skill ID.

```python
bot = loader.get_bot("my-skill")
```

#### `list_available_bots() → List[Dict]`
List all loaded skill bots.

```python
bots = loader.list_available_bots()
# Returns:
# [
#   {
#     "id": "skill-name",
#     "description": "...",
#     "version": "1.0",
#     "tags": ["tag1", "tag2"],
#     "scripts": ["script1.py"]
#   }
# ]
```

#### `search_skills(query: str) → List[Dict]`
Search skills by keyword or tag.

```python
results = loader.search_skills("notification")
# Returns: Matching skills
```

### SkillRegistry

```python
from src.skill_loader import SkillRegistry

registry = SkillRegistry()
```

#### `register(skill: SkillContent) → bool`
Register a loaded skill.

```python
success = registry.register(skill)
```

#### `get_skill(skill_id: str) → Optional[SkillContent]`
Get skill content by ID.

```python
skill = registry.get_skill("my-skill")
```

#### `list_skills() → List[SkillMetadata]`
List all registered skills.

```python
skills = registry.list_skills()
```

#### `find_skills_by_tag(tag: str) → List[SkillContent]`
Find skills with specific tag.

```python
skills = registry.find_skills_by_tag("notification")
```

#### `find_skills_by_keyword(keyword: str) → List[SkillContent]`
Find skills by keyword in name/description.

```python
skills = registry.find_skills_by_keyword("slack")
```

#### `load_module(skill_id: str, script_name: str) → Optional[Any]`
Load Python module from skill script.

```python
module = registry.load_module("my-skill", "handler.py")
result = module.handle_query(query)
```

### PoeSkillRouter

```python
from src.poe_plugin_manager import PoeSkillRouter

router = PoeSkillRouter()
await router.initialize()
```

#### `initialize() → int`
Initialize router with all skills.

```python
count = await router.initialize()
```

#### `route_to_skill(query: str, skill_hint: Optional[str]) → Optional[SkillBot]`
Route query to appropriate skill.

```python
bot = await router.route_to_skill("notify slack", skill_hint=None)
if bot:
    result = await bot.call_with_instructions(query)
```

#### `list_skills() → List[Dict]`
List available skills.

```python
skills = await router.list_skills()
```

#### `search(query: str) → List[Dict]`
Search for skills.

```python
results = await router.search("notification")
```

### Poe Integration

#### HTTP Endpoints

**GET `/skills`**
List all available skill bots.

```bash
curl http://localhost:8000/skills
```

Response:
```json
{
  "total": 5,
  "skills": ["skill-1", "skill-2", "skill-3"]
}
```

**GET `/skills/{skill_id}`**
Get skill details.

```bash
curl http://localhost:8000/skills/my-skill
```

Response:
```json
{
  "id": "my-skill",
  "description": "Skill description"
}
```

**POST `/skills/{skill_id}/execute`**
Execute a skill directly.

```bash
curl -X POST http://localhost:8000/skills/my-skill/execute \
  -H "Content-Type: application/json" \
  -d '{"query": "do something"}'
```

Response:
```json
{
  "result": "Skill result"
}
```

#### Poe Bot Commands

From Poe chat, users can:

**List Skills**
```
@bot list skills
```

**Search Skills**
```
@bot search: notification
```

**Use Specific Skill**
```
Query mentioning skill keyword → Router automatically routes
```

---

## Integration Guide

### 1. Enable Skill Support in Existing Bot

**Before:**
```python
from src.bot import create_app

app = create_app()
```

**After:**
```python
from src.bot_with_skills import create_app_with_skills

app = create_app_with_skills()
```

### 2. Use Skills Programmatically

```python
from src.skill_loader import get_skill_loader

# Initialize
loader = get_skill_loader()
loader.load_all_skills()

# Get skill
bot = loader.get_bot("notification-skill")

# Execute
result = await bot.call_with_instructions("Send Slack notification")
```

### 3. Route Queries to Skills

```python
from src.poe_plugin_manager import PoeSkillRouter

router = PoeSkillRouter()
await router.initialize()

# Route query
bot = await router.route_to_skill("Create beautiful report")

if bot:
    result = await bot.call_with_instructions(query)
```

### 4. Create Dynamic Skill Bots

```python
from src.poe_plugin_manager import get_skill_bot_factory

factory = get_skill_bot_factory()
await factory.initialize()

# Get individual skill bot
skill_bot = factory.get_bot("my-skill")

# Use in Poe
fp.make_app(skill_bot, access_key="...", app=app)
```

---

## Examples

### Example 1: Load and Execute Skill

```python
import asyncio
from src.skill_loader import get_skill_loader

async def example():
    loader = get_skill_loader()
    
    # Load all skills
    count = loader.load_all_skills()
    print(f"Loaded {count} skills")
    
    # Get a skill
    bot = loader.get_bot("notification-skill")
    if bot:
        result = await bot.call_with_instructions(
            "Send Slack notification with test message"
        )
        print(result)

asyncio.run(example())
```

### Example 2: Search and Route

```python
from src.poe_plugin_manager import PoeSkillRouter

async def example():
    router = PoeSkillRouter()
    await router.initialize()
    
    # Search for skills
    results = await router.search("slack")
    print(f"Found {len(results)} skill(s)")
    
    # Route query
    bot = await router.route_to_skill("notify team on slack")
    if bot:
        print(f"Using skill: {bot.name}")

asyncio.run(example())
```

### Example 3: Custom Skill Module

**my-skill/SKILL.md:**
```yaml
---
name: my-skill
description: Custom handler skill
---

# My Skill

Custom instructions...
```

**my-skill/scripts/handler.py:**
```python
def handle_query(query: str) -> str:
    return f"Handled: {query}"
```

**Usage:**
```python
from src.skill_loader import get_skill_loader

loader = get_skill_loader()
loader.load_skill("path/to/my-skill")

module = loader.registry.load_module("my-skill", "handler.py")
result = module.handle_query("test query")
```

---

## Deployment

### Option 1: Run with Skill Support

```bash
# Update modal_app.py to use create_app_with_skills
python -c "from src.bot_with_skills import create_app_with_skills; ..."

# Or
modal deploy modal_app.py
```

### Option 2: Preload Skills

```python
# In modal_app.py or main startup
from src.skill_loader import get_skill_loader

async def initialize():
    loader = get_skill_loader()
    count = loader.load_all_skills()
    print(f"Loaded {count} skills")

# Call before starting Poe
await initialize()
```

### Option 3: Load Skills from Custom Path

```python
loader = get_skill_loader()

# Load from specific directory
custom_skills = loader.load_skill("/custom/skills/path")
```

---

## Status

✅ **Production Ready**

- Full skill discovery and loading
- Poe integration complete
- Dynamic bot creation
- API endpoints
- Error handling
- Logging throughout

---

## Next Steps

1. Add skills to `/home/user/skills/`
2. Update `modal_app.py` to use `create_app_with_skills()`
3. Deploy to Modal/Docker/Local
4. Test skill loading with `/skills` endpoint
5. Use skills from Poe chat

---

**Bl1nk Architect Skill System - Extensible Agent Platform** 🚀
