# Bl1nk Architect Skill System - Complete Guide

**Enable Bl1nk Architect to load Agent Skills as Poe Script Bots**

## What is the Skill System?

The Skill System transforms Bl1nk Architect into a **pluggable platform** where you can:

✅ Load external Agent Skills
✅ Execute skills as Poe bots
✅ Route queries to appropriate skills
✅ Chain multiple skills together
✅ Expose skills via REST API
✅ Create dynamic bots for each skill

## Quick Start (5 minutes)

### Step 1: Enable Skill Support

**File: `src/bot_with_skills.py`**

This file is already created. It provides:
- `Bl1nkArchitectWithSkillsBot` - Enhanced bot with skill routing
- `create_app_with_skills()` - Create FastAPI app with skills
- HTTP endpoints for skill management

### Step 2: Update Modal App (Optional)

**Current:** Uses `src/bot.py` (original)
**New:** Use `src/bot_with_skills.py` (with skills)

```python
# In modal_app.py
from src.bot_with_skills import create_app_with_skills

@asgi_app()
def fastapi_app():
    return create_app_with_skills()
```

### Step 3: Add Skills

Place skills in any directory with `SKILL.md`:

```
/home/user/skills/
├── notification-skill/
│   ├── SKILL.md
│   ├── scripts/
│   │   └── handler.py
│   └── resources/
│       └── templates/
└── analysis-skill/
    ├── SKILL.md
    └── scripts/
        └── analyzer.py
```

**Skill Format (SKILL.md):**
```yaml
---
name: my-skill
description: What this skill does and when to use it
version: 1.0.0
tags:
  - tag1
  - tag2
dependencies:
  - package1
---

# My Skill

Instructions and documentation...
```

### Step 4: Test

```bash
# Start bot
python modal_app.py

# List skills
curl http://localhost:8000/skills

# Execute skill
curl -X POST http://localhost:8000/skills/my-skill/execute \
  -d '{"query": "your query"}'
```

## How It Works

### 1. Skill Discovery

```python
from src.skill_loader import SkillDiscovery

skills = SkillDiscovery.find_skills("/home/user/skills")
skill = SkillDiscovery.parse_skill_file(skill_path)
```

**Discovers:**
- All `SKILL.md` files
- Parses YAML frontmatter
- Finds scripts and resources
- Loads skill metadata

### 2. Skill Registration

```python
from src.skill_loader import SkillRegistry

registry = SkillRegistry()
registry.register(skill)
```

**Manages:**
- Skill metadata
- Script modules
- Resource references
- Skill lookup

### 3. Query Routing

```python
from src.poe_plugin_manager import PoeSkillRouter

router = PoeSkillRouter()
bot = await router.route_to_skill(query)
```

**Routes based on:**
- Explicit skill hints
- Keywords in query
- Tag matching
- Description matching

### 4. Skill Execution

```python
result = await bot.call_with_instructions(query)
```

**Executes:**
- Skill instructions
- Scripts if needed
- Returns formatted result

## Architecture

```
User Query (Poe Chat)
    ↓
Bl1nkArchitectWithSkillsBot
    ├─ Is skill command? → PoeSkillRouter
    ├─ Should use skill? → Route to SkillBot
    └─ Default → Original Analyzer
    ↓
Result (Markdown)
```

## API Reference

### Load Skills

```python
from src.skill_loader import get_skill_loader

loader = get_skill_loader()
count = loader.load_all_skills()
```

### Execute Skill

```python
from src.skill_loader import execute_skill

result = await execute_skill(skill_id, query)
```

### Search Skills

```python
from src.skill_loader import search_skills

results = await search_skills("notification")
```

### Get Available Skills

```python
from src.skill_loader import get_available_skills

skills = await get_available_skills()
```

### Router

```python
from src.poe_plugin_manager import PoeSkillRouter

router = PoeSkillRouter()
await router.initialize()
bot = await router.route_to_skill(query)
```

## Examples

### Example 1: Create Custom Skill

**File: `/home/user/skills/my-skill/SKILL.md`**

```yaml
---
name: my-skill
description: Custom analysis tool for reports
version: 1.0.0
tags:
  - analysis
  - reporting
dependencies:
  - pandas
  - matplotlib
---

# My Analysis Skill

Custom analysis tool.

## Usage

Analyze data and generate reports.

## Implementation

See scripts/analyzer.py
```

**File: `/home/user/skills/my-skill/scripts/analyzer.py`**

```python
def analyze(data):
    return {"result": "analysis complete"}
```

### Example 2: Use Skill from Code

```python
from src.skill_loader import get_skill_loader

loader = get_skill_loader()
loader.load_skill("/home/user/skills/my-skill")

bot = loader.get_bot("my-skill")
result = await bot.call_with_instructions("analyze this")
```

### Example 3: Route Query to Skill

```python
from src.poe_plugin_manager import PoeSkillRouter

router = PoeSkillRouter()
await router.initialize()

# User query
query = "Send Slack notification about analysis"

# Route to skill
bot = await router.route_to_skill(query)

if bot:
    result = await bot.call_with_instructions(query)
```

### Example 4: Use from Poe Chat

```
User: "@bot list skills"
Bot: Shows all available skills

User: "@bot search: notification"
Bot: Shows skills matching "notification"

User: "Send Slack notification with analysis results"
Bot: Routes to notification skill and executes
```

## File Structure

```
src/
├── skill_loader.py          # Skill discovery & loading
├── poe_plugin_manager.py    # Poe bot wrapper
├── bot_with_skills.py       # Enhanced bot with skills
└── bot.py                   # Original bot (unchanged)

example-skills/
└── notification-handler/    # Example skill
    ├── SKILL.md
    └── scripts/
        └── notification_handler.py
```

## HTTP Endpoints

### GET `/skills`
List all available skills

```bash
curl http://localhost:8000/skills
```

### GET `/skills/{skill_id}`
Get skill details

```bash
curl http://localhost:8000/skills/my-skill
```

### POST `/skills/{skill_id}/execute`
Execute a skill

```bash
curl -X POST http://localhost:8000/skills/my-skill/execute \
  -H "Content-Type: application/json" \
  -d '{"query": "do something"}'
```

## Configuration

### Skills Root Directory

Default: `/home/user/skills`

Change in code:
```python
loader = SkillLoader("/custom/path/skills")
```

Or environment variable:
```bash
export SKILLS_ROOT="/custom/path/skills"
```

### Skill Discovery Patterns

Searches for:
- All `SKILL.md` files
- Subdirectories: `scripts/`, `resources/`
- Python files in `scripts/`
- All files in `resources/`

### Loading

- **Lazy loading**: Metadata loaded first
- **On-demand**: Skills loaded when referenced
- **Modules**: Python modules cached in memory

## Production Deployment

### Step 1: Organize Skills

```bash
mkdir -p /home/user/skills
# Add your skills here
```

### Step 2: Update Bot

```python
# modal_app.py
from src.bot_with_skills import create_app_with_skills

@asgi_app()
def fastapi_app():
    return create_app_with_skills()
```

### Step 3: Deploy

```bash
modal deploy modal_app.py
```

### Step 4: Verify

```bash
# Check skills loaded
curl https://your-app.modal.run/skills

# Test skill execution
curl -X POST https://your-app.modal.run/skills/my-skill/execute \
  -d '{"query": "test"}'
```

## Troubleshooting

### No skills found

**Check:**
1. Skills directory exists and has `SKILL.md` files
2. YAML frontmatter is valid
3. Try explicit path: `loader.load_skill("/path/to/skill")`

### Skill not executing

**Check:**
1. Skill is loaded: `/skills` endpoint shows it
2. Query matches skill keywords
3. Scripts have no errors (check logs)

### Module import errors

**Check:**
1. Dependencies are installed
2. Script is valid Python
3. No circular imports

## Next Steps

1. ✅ Review API: `SKILL_SYSTEM_API.md`
2. ✅ Check example: `example-skills/`
3. ✅ Create your skill
4. ✅ Test locally: `python modal_app.py`
5. ✅ Deploy: `modal deploy modal_app.py`

## Support

- **API Reference**: See `SKILL_SYSTEM_API.md`
- **Example Skill**: See `example-skills/notification-handler/`
- **Original Bot**: See `src/bot.py`
- **Complete Docs**: See `COMPLETE_DOCUMENTATION.md`

---

**Bl1nk Architect Skill System - Extensible, Pluggable, Powerful** 🚀
