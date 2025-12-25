# Bl1nk Architect - Quick Start

Full-stack Poe bot analyzing GitHub repos with Gemini Deep Research.

## Setup (5 minutes)

### 1. Install
```
cd bl1nk-architect
pip install -e ".[dev]"
cp .env.example .env
```

### 2. GitHub App
- Visit https://github.com/settings/apps/new
- Create app named "bl1nk-architect"
- Callback: http://localhost:8000/auth/callback
- Permissions: Contents, Repository metadata (Read-only)
- Copy App ID to .env GITHUB_APP_ID
- Generate private key, add to .env GITHUB_PRIVATE_KEY

### 3. Gemini API
- Visit https://ai.google.dev/
- Create API key
- Add to .env GOOGLE_API_KEY

### 4. Poe Setup
- Register at https://poe.com/
- Create bot
- Add access key to .env POE_ACCESS_KEY

### 5. Run
```
python modal_app.py
```

## Deploy to Modal

```
modal secret create bl1nk-secrets \
  POE_ACCESS_KEY="..." \
  GITHUB_APP_ID="..." \
  GITHUB_APP_NAME="bl1nk-architect" \
  GITHUB_PRIVATE_KEY="..." \
  GOOGLE_API_KEY="..."

modal deploy modal_app.py
```

Update GitHub App callback URL to Modal URL.

## Files

- src/bot.py - Poe Protocol
- src/auth.py - GitHub OAuth
- modal_app.py - Serverless entry

## Documentation

- See PROJECT_STRUCTURE.md for architecture
- See ~/docs/poe-protocol/ for Poe Protocol details

