# 🏗️ Bl1nk Architect v2.0

**Enterprise-grade GitHub repository analyzer with intelligent notifications, beautiful reporting, and skill system**

![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Features

### Core Analysis
- 🔍 **8-step repository analysis workflow**
- 📚 **Dependency detection** (Python, TypeScript, Node.js)
- 🔎 **Code duplication detection**
- 🤖 **AI-powered insights** (Gemini Deep Research)

### Notifications (v2.0)
- 📱 **Slack webhooks** - Real-time channel updates
- 🟣 **Linear API** - Automatic issue creation
- ✅ **ClickUp API** - Task management integration

### Widgets (v2.0)
- 📊 **Analysis cards** - Metric visualization
- 📈 **Progress bars** - Visual indicators
- 📋 **Metrics tables** - Organized data
- 🎯 **Dashboard panels** - Complete analysis view

### Skill System (NEW)
- 🔧 **Agent Skills** - Load and execute skills
- 🤖 **Dynamic bots** - Create per-skill Poe bots
- 🔌 **Plugin system** - Extensible architecture
- 📡 **HTTP API** - Rest endpoints

### Development Tools
- 🏥 **Health check system** - 6 comprehensive checks
- 🎨 **Streamlit dashboard** - Real-time monitoring
- 🐳 **Docker setup** - Containerized deployment
- 🧪 **DevContainer** - Local development

---

## 🚀 Quick Start

### Option 1: DevContainer (Recommended)

```bash
# Open in VS Code
# Install "Dev Containers" extension
# Click "Reopen in Container"
```

Or from terminal:
```bash
code --remote-env .devcontainer .
```

### Option 2: Local Setup

```bash
# 1. Clone repository
git clone https://github.com/yourusername/bl1nk-architect.git
cd bl1nk-architect

# 2. Check dependencies
python check_dependencies.py

# 3. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 4. Install dependencies
pip install -e ".[dev]"

# 5. Configure environment
cp .env.example .env
# Edit .env with your credentials

# 6. Run health check
python health_check.py

# 7. Start application
python modal_app.py
```

### Option 3: Docker

```bash
# Build and run with Docker Compose
docker-compose up -d

# Access services:
# - App: http://localhost:8000
# - Monitor: http://localhost:8501
```

---

## 📋 Commands

### Development

```bash
# Check dependencies
python check_dependencies.py

# Run health checks
python health_check.py              # All checks
python health_check.py lint         # Specific check
python health_check.py --json       # JSON output

# Start application
python modal_app.py                 # Local development

# Run dashboard
streamlit run dashboard.py          # Monitoring

# Run tests
pytest tests/

# Format code
black src/ utils/

# Lint
pylint src/
```

### Docker

```bash
# Build images
docker-compose build

# Run services
docker-compose up -d

# View logs
docker-compose logs -f app
docker-compose logs -f monitor

# Stop services
docker-compose down

# Health check from container
docker-compose exec app python health_check.py
```

### Health Endpoints

```bash
# Basic health
curl http://localhost:8000/health

# Full report
curl http://localhost:8000/health/full

# Specific check
curl http://localhost:8000/health/lint
curl http://localhost:8000/health/skills
curl http://localhost:8000/health/webhooks

# HTTP from dashboard
# Open http://localhost:8501
```

---

## 📁 Project Structure

See [STRUCTURE.md](STRUCTURE.md) for detailed breakdown

```
bl1nk-architect/
├── .devcontainer/               # DevContainer config
│   ├── devcontainer.json
│   └── setup.sh
├── src/                         # Source code
│   ├── bot.py                   # Original Poe bot
│   ├── bot_with_skills.py       # Enhanced bot with skills
│   ├── orchestrator_v2.py       # Enhanced workflow
│   ├── health_check.py          # Health checks
│   ├── health_check_api.py      # Health endpoints
│   ├── skill_loader.py          # Skill system
│   ├── poe_plugin_manager.py    # Poe integration
│   ├── notifications/           # Notification system
│   │   ├── notification_manager.py
│   │   ├── slack_notifier.py
│   │   ├── linear_notifier.py
│   │   └── clickup_notifier.py
│   ├── widgets/                 # Widget system
│   │   └── components.py
│   └── ...
├── example-skills/              # Example skills
├── docker-compose.yml           # Docker compose
├── Dockerfile                   # Main app container
├── Dockerfile.dashboard         # Dashboard container
├── dashboard.py                 # Streamlit dashboard
├── health_check.py              # CLI health tool
├── check_dependencies.py        # Dependency checker
├── modal_app.py                 # Modal serverless
├── pyproject.toml               # Dependencies
├── .env.example                 # Environment template
└── README.md                    # This file
```

---

## 🔧 Configuration

### Environment Variables (.env)

```bash
# Core (Required)
POE_ACCESS_KEY=pk_...
GITHUB_APP_ID=123456
GITHUB_PRIVATE_KEY=-----BEGIN PRIVATE KEY-----\n...
GOOGLE_API_KEY=AIza...

# Notifications (Optional)
SLACK_WEBHOOK_URL=https://hooks.slack.com/...
LINEAR_API_KEY=lin_...
CLICKUP_API_KEY=pk_...
```

### Dependency Check

```bash
python check_dependencies.py

# Checks:
# ✓ Python 3.11+
# ✓ Virtual environment
# ✓ All packages
# ✓ .env file
# ✓ Environment variables
# ✓ Required directories
```

---

## 🏥 Health Checks

6 comprehensive checks available:

1. **Health Check** - Service & packages
2. **Lint Check** - Code quality
3. **Skill Check** - Skills system
4. **Webhook Check** - Slack/Linear/ClickUp
5. **GitHub Check** - GitHub App config
6. **Deep Research** - Gemini API

### Run Checks

```bash
# All checks
python health_check.py

# Specific
python health_check.py webhooks

# JSON
python health_check.py --json

# HTTP
curl http://localhost:8000/health/full
```

See [HEALTH_CHECK_GUIDE.md](HEALTH_CHECK_GUIDE.md) for details.

---

## 📊 Dashboard Monitor

Real-time system monitoring with Streamlit:

```bash
# Start dashboard
streamlit run dashboard.py

# Access
# http://localhost:8501

# Features:
# ✓ Overall status
# ✓ Individual check details
# ✓ Auto-refresh capability
# ✓ JSON raw data view
```

See [HEALTH_CHECK_GUIDE.md](HEALTH_CHECK_GUIDE.md#streamlit-dashboard) for details.

---

## 🐳 Docker Deployment

Two containerized services:

### Service 1: Main Application
```bash
docker-compose up app

# Runs on port 8000
# Health check: http://localhost:8000/health
```

### Service 2: Dashboard Monitor
```bash
docker-compose up monitor

# Runs on port 8501
# Access: http://localhost:8501
```

### Both Services
```bash
docker-compose up

# Access:
# - App: http://localhost:8000
# - Monitor: http://localhost:8501
```

See [Dockerfile](Dockerfile) and [Dockerfile.dashboard](Dockerfile.dashboard)

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| [COMPLETE_DOCUMENTATION.md](COMPLETE_DOCUMENTATION.md) | Everything (2,001 lines) |
| [STRUCTURE.md](STRUCTURE.md) | Project structure |
| [HEALTH_CHECK_GUIDE.md](HEALTH_CHECK_GUIDE.md) | Health system |
| [SKILL_SYSTEM_GUIDE.md](SKILL_SYSTEM_GUIDE.md) | Skill system |
| [SKILL_SYSTEM_API.md](SKILL_SYSTEM_API.md) | Skill API reference |
| [SKILL.md](SKILL.md) | Agent Skill wrapper |

---

## 🔌 Integrations

### Poe Chat Bot
```python
from src.bot_with_skills import create_app_with_skills

app = create_app_with_skills()
```

### Slack
```python
from src.notifications import get_notification_manager

nm = get_notification_manager()
nm.register_slack(user_id, webhook_url)
```

### Linear
```python
nm.register_linear(user_id, api_key, team_id, project_id)
```

### ClickUp
```python
nm.register_clickup(user_id, api_key, project_id)
```

See [COMPLETE_DOCUMENTATION.md](COMPLETE_DOCUMENTATION.md) for full API.

---

## 🚢 Deployment

### Modal Cloud
```bash
modal secret create bl1nk-secrets \
  POE_ACCESS_KEY="..." \
  GITHUB_APP_ID="..." \
  ...

modal deploy modal_app.py
```

### Docker
```bash
docker-compose up -d
```

### Local
```bash
python modal_app.py
```

---

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# With coverage
pytest --cov=src tests/

# Specific test
pytest tests/test_bot.py
```

---

## 📝 Development

### Adding Skills
1. Create `/home/user/skills/my-skill/SKILL.md`
2. Add YAML frontmatter
3. Add scripts in `scripts/` folder
4. Bot auto-discovers

### Adding Notifications
1. Create notifier in `src/notifications/`
2. Implement `send_notification()` method
3. Register in `NotificationManager`
4. Update documentation

---

## 🤝 Contributing

1. Fork repository
2. Create feature branch
3. Make changes
4. Run: `python check_dependencies.py`
5. Run: `python health_check.py`
6. Submit pull request

---

## 📄 License

MIT License - See [LICENSE.txt](LICENSE.txt)

---

## 🆘 Support

### Quick Help
- **Setup issues?** → Run `python check_dependencies.py`
- **Configuration?** → Check `.env.example`
- **Errors?** → See [HEALTH_CHECK_GUIDE.md](HEALTH_CHECK_GUIDE.md)
- **API questions?** → See [COMPLETE_DOCUMENTATION.md](COMPLETE_DOCUMENTATION.md)

### Resources
- 📖 Documentation - See docs folder
- 🐛 Issues - GitHub issues
- 💬 Discussions - GitHub discussions

---

## 🎯 Next Steps

1. ✅ [Run dependency check](check_dependencies.py)
2. ✅ [Configure .env](.env.example)
3. ✅ [Run health check](health_check.py)
4. ✅ [Start local development](#quick-start)
5. ✅ [Monitor dashboard](#dashboard-monitor)
6. ✅ [Deploy](#deployment)

---

**Ready to ship! 🚀**

*Bl1nk Architect - Enterprise Repository Analysis Platform*
