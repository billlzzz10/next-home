# Bl1nk Architect - Health Check Guide

**Comprehensive system health and configuration verification**

---

## Overview

The Health Check System verifies 6 critical components:

1. **Health Check** - Basic service health & dependencies
2. **Lint Check** - Code quality and syntax
3. **Skill Check** - Skills discovery and loading
4. **Webhook Check** - Slack/Linear/ClickUp connectivity
5. **GitHub Check** - GitHub App configuration
6. **Deep Research Check** - Gemini API connectivity

---

## Quick Start

### Run All Checks

```bash
python health_check.py
```

**Output:**
```
🏥 BL1NK ARCHITECT HEALTH CHECK
==================================================
Time: 2024-12-16 16:00:00

📊 SUMMARY
  Total Checks: 6
  OK: 4 ✓
  Warnings: 1 ⚠
  Errors: 0 ✗

Overall Status: ⚠ WARNING
...
```

### Quick Check (Packages Only)

```bash
python health_check.py --quick
```

### Specific Check

```bash
python health_check.py lint          # Lint check
python health_check.py skills        # Skills check
python health_check.py webhooks      # Webhooks check
python health_check.py github        # GitHub check
python health_check.py deepresearch  # Gemini check
```

### JSON Output

```bash
python health_check.py --json

# Or for specific check
python health_check.py lint --json
```

---

## Health Checks Explained

### 1. Health Check (Basic)

**What it checks:**
- Python version
- Required packages installed
- Dependencies availability

**Configuration needed:**
None - checks built-in requirements

**Success indicators:**
- ✓ All required packages installed
- Python 3.11+

**Common issues:**
- Missing package → Install with `pip install -e ".[dev]"`
- Python version < 3.11 → Upgrade Python

### 2. Lint Check (Code Quality)

**What it checks:**
- Python syntax errors
- Code structure issues
- Line length (>120 chars)
- Tab usage (should use spaces)
- File size

**Files checked:**
- All `.py` files in `src/`

**Configuration needed:**
None - automated analysis

**Success indicators:**
- ✓ No syntax errors
- ✓ No long lines (>120)
- ✓ No tabs

**Common issues:**
- Syntax error → Fix Python code
- Long lines → Break into multiple lines
- Tab characters → Replace with spaces

### 3. Skill Check (Skills System)

**What it checks:**
- Skills discovered
- SKILL.md parsing
- Metadata extraction
- Script availability

**Directories checked:**
- `/home/user/skills/`
- `/home/user/projects/bl1nk-architect/example-skills/`

**Configuration needed:**
Optional - skills in `/home/user/skills/`

**Success indicators:**
- ✓ Skills discovered
- ✓ All skills parsed successfully
- ✓ Scripts found

**Common issues:**
- No skills found → Create in `/home/user/skills/`
- Parse errors → Check SKILL.md format
- Invalid YAML → Fix frontmatter

### 4. Webhook Check (Platform Integration)

**What it checks:**
- Slack webhook connectivity
- Linear API authentication
- ClickUp API authentication

**Platforms:**
- Slack (HTTP POST to webhook)
- Linear (GraphQL query)
- ClickUp (REST GET)

**Configuration needed (optional):**
```bash
export SLACK_WEBHOOK_URL="https://hooks.slack.com/..."
export LINEAR_API_KEY="lin_..."
export CLICKUP_API_KEY="pk_..."
```

**Success indicators:**
- ✓ Webhook URLs respond (200)
- ✓ API authentication succeeds
- ✓ Network connectivity OK

**Common issues:**
- 404 error → Webhook URL invalid
- 401 error → API key invalid
- Timeout → Network issue or invalid URL

**Fix:**
```bash
# Test Slack webhook
curl -X POST https://hooks.slack.com/services/YOUR/WEBHOOK/URL \
  -H 'Content-Type: application/json' \
  -d '{"text":"Test"}'

# Test Linear API
curl https://api.linear.app/graphql \
  -H "Authorization: Bearer lin_YOUR_KEY" \
  -d '{"query":"{ viewer { id } }"}'

# Test ClickUp API
curl https://api.clickup.com/api/v2/user \
  -H "Authorization: pk_YOUR_KEY"
```

### 5. GitHub Check (GitHub App)

**What it checks:**
- GitHub App ID configured
- Private key present
- Private key format valid
- App name set

**Configuration needed (required for bot):**
```bash
export GITHUB_APP_ID="123456"
export GITHUB_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n..."
export GITHUB_APP_NAME="bl1nk-architect"
```

**Success indicators:**
- ✓ App ID valid
- ✓ Private key present and valid format
- ✓ App name configured

**Common issues:**
- Missing App ID → Get from GitHub settings
- Invalid key → Check RSA private key format
- Key not loaded → Verify environment variable

**Fix:**
1. Go to https://github.com/settings/apps
2. Create or select app
3. Copy App ID to environment
4. Generate private key and save
5. Base64 encode and set as environment variable

### 6. Deep Research Check (Gemini API)

**What it checks:**
- Gemini API key configured
- API authentication
- Model availability

**Configuration needed (required for analysis):**
```bash
export GOOGLE_API_KEY="AIza..."
```

**Success indicators:**
- ✓ API key present
- ✓ Authentication successful
- ✓ Model accessible

**Common issues:**
- Missing API key → Get from https://ai.google.dev/
- Invalid key → Regenerate key
- API error → Check quota/billing

**Fix:**
```bash
# Get API key
# Visit https://ai.google.dev/
# Create new API key
export GOOGLE_API_KEY="your-key"

# Test
python -c "import google.genai; google.genai.configure(api_key='your-key')"
```

---

## HTTP Endpoints

### GET `/health`
Basic health check

```bash
curl http://localhost:8000/health
```

**Response (healthy):**
```json
{
  "status": "healthy",
  "overall_status": "ok"
}
```

### GET `/health/full`
Complete report

```bash
curl http://localhost:8000/health/full
```

### GET `/health/summary`
Summary only

```bash
curl http://localhost:8000/health/summary
```

### GET `/health/status/{check_name}`
Specific check

```bash
curl http://localhost:8000/health/status/lint
curl http://localhost:8000/health/status/webhooks
```

### GET `/health/{check}`
Shortcut endpoints

```bash
curl http://localhost:8000/health/lint
curl http://localhost:8000/health/skills
curl http://localhost:8000/health/webhooks
curl http://localhost:8000/health/github
curl http://localhost:8000/health/deepresearch
```

---

## Integration with Bot

### Enable Health Checks in Modal App

```python
# modal_app.py
from src.health_check_api import include_health_routes

@asgi_app()
def fastapi_app():
    from src.bot_with_skills import create_app_with_skills
    app = create_app_with_skills()
    
    # Add health check routes
    include_health_routes(app)
    
    return app
```

### Monitor Health in Production

```bash
# Check every 30 seconds
while true; do
  curl -s http://localhost:8000/health | jq .
  sleep 30
done

# Or specific check
curl http://localhost:8000/health/status/webhooks | jq .
```

---

## Using as Library

### Import and Run

```python
from src.health_check import run_health_check

async def check_system():
    result = await run_health_check()
    print(result)
```

### Check Specific Component

```python
from src.health_check import get_health_checker

checker = get_health_checker()
await checker.check_skills()
result = checker.results["Skill Check"]
```

---

## Troubleshooting Guide

### Issue: "Missing packages"

**Cause:** Not all dependencies installed

**Fix:**
```bash
cd /home/user/projects/bl1nk-architect
pip install -e ".[dev]"
```

### Issue: "Lint errors found"

**Cause:** Code quality issues

**Fix:**
```bash
# Format code
black src/

# Check style
pylint src/

# Fix issues manually based on output
```

### Issue: "No skills found"

**Cause:** Skills not in expected location

**Fix:**
```bash
mkdir -p /home/user/skills
# Add your SKILL.md files here
```

### Issue: "Webhook errors"

**Cause:** Invalid credentials or network issue

**Fix:**
1. Verify webhook/API URL is correct
2. Test independently (see examples above)
3. Check firewall/network access
4. Regenerate API keys if needed

### Issue: "GitHub check failed"

**Cause:** Missing or invalid configuration

**Fix:**
```bash
# Check environment
echo $GITHUB_APP_ID
echo $GITHUB_PRIVATE_KEY

# If missing, get from GitHub:
# https://github.com/settings/apps
```

### Issue: "Gemini API error"

**Cause:** Invalid key or quota exceeded

**Fix:**
1. Verify API key at https://ai.google.dev/
2. Check billing/quota status
3. Try with different model
4. Regenerate key if needed

---

## Status Codes

| Status | Meaning | Action |
|--------|---------|--------|
| ✓ OK | Working perfectly | None needed |
| ⚠ WARNING | Working but has issues | Monitor |
| ✗ ERROR | Not working | Fix immediately |
| ○ UNCONFIGURED | Optional feature not set | Optional |

---

## Production Checklist

Before deploying to production:

- [ ] Run `python health_check.py`
- [ ] All checks show ✓ OK or acceptable ⚠
- [ ] No ✗ ERROR status
- [ ] GitHub configured
- [ ] Webhooks tested
- [ ] Gemini API working
- [ ] Health endpoints accessible
- [ ] Monitor logs for issues

---

## Examples

### Example 1: Test Before Deployment

```bash
python health_check.py

# Check for any errors
# Fix issues if found
# Deploy when all OK
```

### Example 2: Monitor Health

```bash
# In production
curl -X GET http://localhost:8000/health/full | \
  python -m json.tool | \
  grep -E '"status"|"overall_status"'
```

### Example 3: Specific Component Test

```bash
# Test only webhooks
python health_check.py webhooks

# Test only GitHub
python health_check.py github
```

### Example 4: Integration Check

```bash
# Run in CI/CD pipeline
python health_check.py --json > health_report.json

# Exit with error if any failures
jq '.overall_status' health_report.json | grep -q "error" && exit 1
```

---

## Files

- **health_check.py** - CLI tool
- **src/health_check.py** - Core check logic
- **src/health_check_api.py** - HTTP endpoints

---

## Next Steps

1. Run: `python health_check.py`
2. Fix any errors
3. Enable health endpoints in bot
4. Monitor regularly

---

**Ready to ship with confidence!** ✅
