# GitHub Actions Setup Guide

## Quick Setup

### 1. Add GitHub Secrets

```
Settings → Secrets and variables → Actions
```

Add these secrets:

```
MODAL_TOKEN_ID=your_token_id
MODAL_TOKEN_SECRET=your_token_secret
SLACK_WEBHOOK_URL=your_slack_webhook (optional)
DOCKER_USERNAME=your_docker_username (optional)
DOCKER_PASSWORD=your_docker_password (optional)
```

### 2. Workflows Included

**deploy.yml** - Deploy to Modal on push to main/develop
**test.yml** - Run tests on every push
**security-scan.yml** - Security checks (Bandit, CodeQL)
**code-quality.yml** - Code quality (Ruff, Black, mypy)
**docker-build.yml** - Build Docker image
**release.yml** - Create releases on version tags

### 3. Deploy

```bash
# Auto-deploy to staging
git push origin develop

# Auto-deploy to production
git push origin main

# Create release
git tag v1.0.0
git push origin v1.0.0
```

### 4. Monitor

Go to: **Actions tab → Select workflow → View runs**

## Troubleshooting

**Deployment fails?**
- Check logs in Actions tab
- Verify Modal secrets are set
- Run `pytest tests/` locally first

**Tests failing?**
- Run `pytest tests/ -v` locally
- Fix issues, commit, push

**Docker build fails?**
- Check Docker Hub credentials
- Verify Dockerfile syntax

## Cost

GitHub Actions free:
- 2,000 minutes/month (public repos)
- 3,000 minutes/month (private repos)

