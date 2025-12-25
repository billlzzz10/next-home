# GitHub Push Guide - BL1NK Skill MCP Server

## 📋 เตรียมการ

ไฟล์ทั้งหมดอยู่ใน git แล้ว พร้อมที่จะ push ไปที่ GitHub

### ตรวจสอบ
```bash
cd /home/user/mcp-servers/bl1nk-skill-mcp-server
git status
git log --oneline -3
```

## 🚀 วิธี Push (เลือก 1 วิธี)

### ✅ วิธี 1: ใช้ Helper Script (แนะนำ)

```bash
cd /home/user/mcp-servers/bl1nk-skill-mcp-server

# Step 1: สร้าง GitHub Personal Access Token
# ไปที่ https://github.com/settings/tokens
# - Click "Generate new token (classic)"
# - Name: "bl1nk-push"
# - Scopes: repo, read:org
# - Copy token

# Step 2: Push
./scripts/github-push.sh "YOUR_TOKEN_HERE"

# Or use environment variable
export GITHUB_TOKEN="YOUR_TOKEN_HERE"
./scripts/github-push.sh
```

### ✅ วิธี 2: ใช้ Git Credentials

```bash
cd /home/user/mcp-servers/bl1nk-skill-mcp-server

# Enable credentials storage
git config credential.helper store

# Push (system will ask for username & password)
git push origin main

# When prompted enter:
# Username: billlzzz10
# Password: YOUR_GITHUB_TOKEN
```

### ✅ วิธี 3: SSH (ถ้ามี SSH key ตั้งไว้)

```bash
cd /home/user/mcp-servers/bl1nk-skill-mcp-server

# Change remote to SSH
git remote set-url origin git@github.com:billlzzz10/bl1nk-skill-mcp-server.git

# Push
git push origin main
```

## 📊 สิ่งที่จะ Push

### Code Fixes (5 files)
- ✅ `src/server.py` - Fixed delete_skill scope
- ✅ `src/api.py` - Added DELETE endpoint
- ✅ `src/cli.py` - Full CLI implementation
- ✅ `src/__init__.py` - Package init (NEW)
- ✅ `src/__main__.py` - Module entry (NEW)

### Docker Fixes (4 files)
- ✅ `docker/Dockerfile` - Health check + deps
- ✅ `docker/docker-compose.yml` - Optional services
- ✅ `.dockerignore` - Size optimization (NEW)
- ✅ `docker/.env.example` - Config template (NEW)

### Automation Scripts (2 files)
- ✅ `scripts/release.sh` - Release automation (600+ lines)
- ✅ `scripts/docker-build.sh` - Docker helper (400+ lines)
- ✅ `scripts/github-push.sh` - GitHub push helper (NEW)

### Documentation (7 files)
- ✅ `IMPROVEMENTS.md` - Code fixes detailed
- ✅ `VERIFICATION_REPORT.md` - Quality report
- ✅ `QUICKSTART.md` - Getting started
- ✅ `FIX_INDEX.md` - Feature navigation
- ✅ `DOCKER_GUIDE.md` - Docker guide
- ✅ `RELEASE_GUIDE.md` - Release process
- ✅ `DOCKER_AND_RELEASE_SUMMARY.md` - Summary

**Total: 26 files + documentation**

## ✅ After Push

### 1. Verify on GitHub
```
https://github.com/billlzzz10/bl1nk-skill-mcp-server
```

### 2. Check Files
- All Python files updated
- All scripts executable
- All docs visible

### 3. Create Release (Optional)
```bash
./scripts/release.sh 1.0.0
```

## 📝 GitHub Token

### Create Token Steps:
1. Go to: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Name it: "bl1nk-push"
4. Select scopes:
   - ✅ repo (full control)
   - ✅ read:org
5. Click "Generate"
6. Copy the token (appears only once)

### Use Token:
```bash
# Option A: Command line
./scripts/github-push.sh "ghp_xxxxxxxxxxxxxxxxxxxx"

# Option B: Environment variable
export GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxx"
./scripts/github-push.sh

# Option C: Git config
git config credential.helper store
git push origin main  # Will ask for token as password
```

## 🔐 Security Notes

⚠️ **Never commit tokens to repository!**
- Tokens are temporary
- Delete token after use
- Use environment variables in CI/CD
- Keep tokens in `.env` files (in .gitignore)

## 🐛 Troubleshooting

### "Permission denied"
→ Token doesn't have `repo` scope
→ Create new token with correct scopes

### "Invalid token"
→ Check token is correct
→ Token may have expired
→ Create new token from https://github.com/settings/tokens

### "Nothing to commit"
→ All changes already tracked
→ Just push: `git push origin main`

### "Diverged history"
→ Run: `git pull --rebase origin main`
→ Then: `git push origin main`

## 📞 Help

For issues with:
- **Git**: `git help push`
- **GitHub tokens**: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens
- **SSH keys**: https://docs.github.com/en/authentication/connecting-to-github-with-ssh

---

**Ready? Choose your method above and push! 🚀**
