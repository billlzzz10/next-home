# Project Structure

**Bl1nk Architect v2.0 - Complete File Organization**

---

## Root Level

```
bl1nk-architect/
├── .devcontainer/              # 🐳 Local DevContainer
│   ├── devcontainer.json       # VSCode configuration
│   └── setup.sh                # Setup script
├── .github/                    # 📋 GitHub
│   └── workflows/              # CI/CD workflows
├── src/                        # 💻 Source code (main)
├── example-skills/             # 🎓 Example implementations
├── tests/                      # 🧪 Unit tests
├── logs/                       # 📝 Logs directory
├── data/                       # 💾 Data directory
├── skills/                     # 🔧 User skills (external)
│
├── docker-compose.yml          # 🐳 Docker services
├── Dockerfile                  # 🐳 Main app container
├── Dockerfile.dashboard        # 🐳 Dashboard container
│
├── modal_app.py                # 🚀 Modal serverless
├── health_check.py             # 🏥 CLI health tool
├── check_dependencies.py       # 📦 Dependency checker
├── dashboard.py                # 📊 Streamlit dashboard
│
├── README.md                   # 📖 Main guide
├── STRUCTURE.md                # 📋 This file
├── COMPLETE_DOCUMENTATION.md   # 📚 Complete docs
├── HEALTH_CHECK_GUIDE.md       # 🏥 Health checks
├── SKILL_SYSTEM_GUIDE.md       # 🔧 Skills guide
├── SKILL_SYSTEM_API.md         # 🔌 Skills API
│
├── pyproject.toml              # 📦 Dependencies
├── .env.example                # ⚙️ Environment template
├── .gitignore                  # 🚫 Git ignore
└── LICENSE.txt                 # 📄 MIT License
```

---

## src/ - Source Code

### Core Bot
```
src/
├── bot.py                      # 🤖 Original Poe bot interface
│   ├── Bl1nkArchitectBot class
│   ├── get_response() - Handles queries
│   ├── get_settings() - Bot metadata
│   └── create_app() - FastAPI factory
│
├── bot_with_skills.py          # 🤖 Enhanced bot with skills
│   ├── Bl1nkArchitectWithSkillsBot
│   ├── Skill command routing
│   ├── HTTP endpoints (/skills)
│   └── create_app_with_skills()
│
└── modal_app.py                # 🚀 Modal serverless entry
    ├── Image configuration
    ├── Function decoration
    └── ASGI app setup
```

### Analysis Engine
```
src/
├── orchestrator.py             # 🔄 Original v1 workflow (8 steps)
├── orchestrator_v2.py          # 🔄 Enhanced v2 with notifications
├── gemini_client.py            # 🧠 Gemini Deep Research
├── github_client.py            # 📡 GitHub API client
└── auth.py                     # 🔐 GitHub OAuth flow
```

### Notification System (v2.0)
```
src/notifications/
├── __init__.py                 # Package exports
├── notification_manager.py     # 📤 Central orchestrator
│   ├── NotificationChannel enum
│   ├── NotificationPreference dataclass
│   ├── NotificationRegistry class
│   └── NotificationManager class
├── slack_notifier.py           # 📱 Slack webhooks
│   └── SlackNotifier class
├── linear_notifier.py          # 🟣 Linear API
│   └── LinearNotifier class
└── clickup_notifier.py         # ✅ ClickUp API
    └── ClickUpNotifier class
```

### Widget System (v2.0)
```
src/widgets/
├── __init__.py                 # Package exports
└── components.py               # 🎨 All widgets
    ├── AnalysisCard
    ├── ProgressBar
    ├── MetricsRow
    ├── AnalysisPanel
    ├── WidgetStyle enum
    └── create_analysis_report()
```

### Skill System (NEW)
```
src/
├── skill_loader.py             # 🔧 Skill discovery & loading (423 lines)
│   ├── SkillMetadata dataclass
│   ├── SkillContent dataclass
│   ├── SkillDiscovery class
│   ├── SkillRegistry class
│   ├── SkillLoader class
│   └── Global API functions
│
├── poe_plugin_manager.py       # 🔌 Poe integration (358 lines)
│   ├── PoeSkillRouter class
│   ├── PoeSkillBot class
│   ├── DynamicSkillBot class
│   ├── DynamicSkillBotFactory class
│   └── Global factory instance
│
└── attachment_handler.py       # 📎 File management
    ├── prepare_markdown_file()
    └── handle_attachments()
```

### Health Check System
```
src/
├── health_check.py             # 🏥 Core checks (563 lines)
│   ├── HealthCheckResult dataclass
│   ├── HealthChecker class
│   │   ├── check_basic_health()
│   │   ├── check_lint()
│   │   ├── check_skills()
│   │   ├── check_webhooks()
│   │   ├── check_github()
│   │   └── check_deep_research()
│   └── Global API functions
│
└── health_check_api.py         # 📡 HTTP endpoints (235 lines)
    ├── /health
    ├── /health/full
    ├── /health/summary
    ├── /health/status/{check}
    └── /health/{check} shortcuts
```

### Utilities
```
src/
├── introduction_manager.py     # 📝 Welcome messages
└── attachment_handler.py       # 📎 File handling

utils/
├── __init__.py
├── formatter.py                # 📋 Output formatting
└── widgets.py                  # 🎨 Widget utilities
```

---

## .devcontainer/

Development container configuration:

```
.devcontainer/
├── devcontainer.json           # VSCode configuration
│   ├── Python 3.11 image
│   ├── Extensions
│   ├── Port forwarding (8000, 8501, 5000)
│   └── Post-create script
│
└── setup.sh                    # Initialization script
    ├── Creates venv
    ├── Installs dependencies
    ├── Creates .env
    ├── Creates directories
    └── Runs health check
```

---

## Docker

```
Dockerfile                      # Main application
├── python:3.11-slim base
├── System dependencies
├── Project files copy
├── Dependency installation
├── Directories creation
├── Healthcheck setup
└── Entry command

Dockerfile.dashboard           # Dashboard monitor
├── python:3.11-slim base
├── System dependencies
├── Project files copy
├── Streamlit-specific deps
└── Streamlit run command

docker-compose.yml            # Orchestration
├── app service (port 8000)
├── monitor service (port 8501)
├── Networking setup
├── Volume mounts
├── Health checks
└── Environment variables
```

---

## Tools & Scripts

```
Root Level Scripts:

health_check.py                # 🏥 CLI health checker
├── Python version check
├── Virtual environment check
├── Package check
├── .env verification
├── Environment variables check
└── Colored output

check_dependencies.py          # 📦 Dependency verifier
├── Python version (3.11+)
├── Virtual environment
├── Required packages
├── .env file
├── Environment variables
├── Directories
└── Required files

dashboard.py                   # 📊 Streamlit monitor
├── Real-time health display
├── Per-check details
├── Auto-refresh
├── JSON export
└── Status indicators

modal_app.py                   # 🚀 Modal serverless
├── Image building
├── Function decoration
├── Secret mounting
├── ASGI setup
└── Entry point
```

---

## Documentation

```
COMPLETE_DOCUMENTATION.md      # 📚 Everything (2,001 lines)
├── Overview & changelog
├── Architecture
├── Notification system
├── Widget system
├── Enhanced orchestrator
├── Installation & setup
├── API reference
├── Integration guides
├── Deployment
├── Testing
└── Troubleshooting

HEALTH_CHECK_GUIDE.md         # 🏥 Health system (523 lines)
├── Quick start
├── 6 check explanations
├── Configuration needed
├── Success indicators
├── Common issues & fixes
├── HTTP endpoints
├── Library usage
└── Production checklist

SKILL_SYSTEM_GUIDE.md         # 🔧 Skills guide (437 lines)
├── Quick start
├── Architecture
├── Component reference
├── Integration guides
├── Examples
├── Deployment
└── Troubleshooting

SKILL_SYSTEM_API.md           # 🔌 Skills API (527 lines)
├── Overview
├── Architecture
├── API reference
├── HTTP endpoints
├── Examples
└── Deployment

SKILL.md                       # 🤖 Agent Skill wrapper
├── YAML frontmatter
├── When to use
├── Component list
├── Quick examples
└── Integration info
```

---

## example-skills/

Example skill implementations:

```
example-skills/
└── notification-handler/      # 📬 Notification example
    ├── SKILL.md               # Skill definition
    │   └── YAML frontmatter
    │
    └── scripts/
        └── notification_handler.py
            ├── handle_slack_notification()
            ├── handle_linear_issue()
            ├── handle_clickup_task()
            └── execute()
```

---

## tests/

Unit tests:

```
tests/
├── __init__.py
├── test_bot.py                 # Bot tests
├── test_auth.py                # Auth tests
├── test_orchestrator.py        # Orchestrator tests
├── test_notifications.py       # Notification tests
├── test_widgets.py             # Widget tests
├── test_skills.py              # Skill tests
└── test_health_check.py        # Health check tests
```

---

## Configuration Files

```
pyproject.toml                 # 📦 Dependencies & build config
├── Project metadata
├── Core dependencies
├── Optional dev dependencies
├── Build system
└── Tool configurations

.env.example                   # ⚙️ Environment template
├── POE_ACCESS_KEY
├── GITHUB_APP_ID
├── GITHUB_PRIVATE_KEY
├── GOOGLE_API_KEY
├── Slack/Linear/ClickUp keys
└── Optional settings

.gitignore                     # 🚫 Git ignore patterns
├── venv/
├── __pycache__/
├── .env
├── .env.local
└── IDE files
```

---

## Size & Metrics

| Component | Files | Lines | Purpose |
|-----------|-------|-------|---------|
| **Core** | 6 | 1,500+ | Main functionality |
| **Notifications** | 5 | 400+ | Platform integration |
| **Widgets** | 2 | 450+ | UI components |
| **Skills** | 3 | 1,010 | Plugin system |
| **Health** | 2 | 798 | Diagnostics |
| **Docs** | 5 | 3,500+ | Documentation |
| **Docker** | 4 | 200+ | Containerization |
| **Config** | 3 | 150+ | Configuration |
| **TOTAL** | 30+ | 8,000+ | Complete system |

---

## Data Flow

### Query Processing
```
User Query (Poe/HTTP)
    ↓
Bot Handler
    ├─ Skill routing
    ├─ Authentication
    └─ Original analyzer
    ↓
Analysis Engine
    ├─ GitHub Client
    ├─ Gemini Research
    └─ Data collection
    ↓
Widget System
    ├─ Create components
    └─ Format report
    ↓
Notification System
    ├─ Slack
    ├─ Linear
    └─ ClickUp
    ↓
User Response
```

### Health Check Flow
```
CLI / HTTP Request
    ↓
HealthChecker
    ├─ Check 1: Basic
    ├─ Check 2: Lint
    ├─ Check 3: Skills
    ├─ Check 4: Webhooks
    ├─ Check 5: GitHub
    └─ Check 6: Deep Research
    ↓
Result Aggregation
    ├─ Status determination
    ├─ Summary generation
    └─ Formatting
    ↓
Output
    ├─ Console (colored)
    ├─ JSON (API)
    ├─ Dashboard (streaming)
    └─ HTTP (endpoints)
```

---

## Development Workflow

### Local Development
```
1. Clone/pull code
2. Run: python check_dependencies.py
3. Configure: .env file
4. Run: python health_check.py
5. Start: python modal_app.py
6. Monitor: streamlit run dashboard.py
```

### DevContainer Development
```
1. Open in DevContainer
2. Auto-setup runs (setup.sh)
3. VSCode extensions load
4. Run: python health_check.py
5. Start: python modal_app.py
6. Monitor: streamlit run dashboard.py
```

### Docker Development
```
1. Build: docker-compose build
2. Run: docker-compose up
3. Monitor: docker-compose logs
4. Access: http://localhost:8000 & 8501
5. Health: docker-compose exec app python health_check.py
```

---

## Dependencies

### Core
- fastapi-poe (Poe protocol)
- modal (serverless)
- google-genai (Gemini)
- PyGithub (GitHub)

### Web
- fastapi (API)
- httpx (HTTP)
- streamlit (dashboard)

### Config
- python-dotenv (.env)
- pyyaml (YAML)
- cryptography (keys)

### Dev
- pytest (testing)
- black (formatting)
- pylint (linting)

---

## Access Patterns

### By Role

**Developer**
- Focus: `src/`, `tests/`
- Read: `COMPLETE_DOCUMENTATION.md`

**DevOps**
- Focus: `docker-compose.yml`, `Dockerfile*`
- Read: `STRUCTURE.md`, `README.md`

**Data Scientist**
- Focus: `src/orchestrator_v2.py`, `src/gemini_client.py`
- Read: `COMPLETE_DOCUMENTATION.md`

**Product Owner**
- Focus: `README.md`, health endpoints
- Read: `COMPLETE_DOCUMENTATION.md`

---

**Last Updated**: December 2024
**Version**: 2.0.0
**Status**: Production Ready ✅
