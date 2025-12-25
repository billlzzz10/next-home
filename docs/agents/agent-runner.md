# 🚀 Agent Orchestration Runner

## System Overview

This directory contains 7 agent system prompts that work together to manage the bl1nk / BLinkOS project:

```
┌─────────────────────────────────────────────────────────────┐
│                    Project Manager Agent                     │
│  (Receives requirements → Distributes to specialized agents) │
└──────────────┬──────────────────────────────────────────────┘
               │
       ┌───────┼───────┬──────────┬──────────┐
       ▼       ▼       ▼          ▼          ▼
    Arch   OAuth   Reviewer   Document   CI/CD
   Design  Workspace           Writer   Deploy
       │       │        │          │      │
       └───────┴────────┴──────────┴──────┘
               │
       ┌───────▼──────────┐
       │ Telemetry Agent  │
       │ (Feedback Loop)  │
       └──────────────────┘
```

## How to Use

### 1. **Load Agent Prompts**
Each agent file contains its system prompt. When using with Claude or another LLM:

```bash
# Copy the content of any SYSTEM_PROMPT_*.md file
# Paste it as system context when creating an agent instance
```

### 2. **Agent Workflow Example**

**Input (from user/PM):**
```
"I need to add a new Dashboard component to the web app with OAuth integration"
```

**PM Agent receives → Breaks down into tasks:**
```
TASK-001: [Architecture] Determine where dashboard component lives
TASK-002: [OAuth] Setup user context/workspace binding
TASK-003: [Code] Create dashboard UI component
TASK-004: [Review] Verify code quality & TypeScript
TASK-005: [Docs] Write component documentation
TASK-006: [CI/CD] Ensure pipeline passes
TASK-007: [Telemetry] Setup analytics tracking
```

**Each agent executes their task:**
- Architecture: Returns component placement + imports needed
- OAuth: Returns user object structure + auth flow
- Reviewer: Validates code against standards
- Document Writer: Creates README for component
- CI/CD: Tests build process
- Telemetry: Defines tracking events

**Feedback Loop:**
- Telemetry Agent collects issues found during integration
- Reports back to PM for next iteration

### 3. **Running with Multi-Agent System**

You can integrate these with:
- **LangChain** (Python/JS)
- **OpenAI API** (with function calling)
- **Custom orchestrator** (Node.js/Python runner)

Example architecture:
```
User Input
    ↓
PM Agent (routes to specialists)
    ↓
[Parallel execution of relevant agents]
    ↓
Results aggregated
    ↓
Telemetry feedback
    ↓
Next action recommendations
```

### 4. **Output Templates**

Each agent outputs in their specified format:
- **PM**: Task list with status
- **Architecture**: File location + import paths
- **OAuth**: API spec + flow diagram
- **Reviewer**: Pass/Fail + recommendations
- **Document Writer**: Markdown docs
- **CI/CD**: Build status + pipeline report
- **Telemetry**: Events summary + alerts

## Integration Checklist

- [ ] Set up your LLM API (OpenAI, Claude, etc.)
- [ ] Load each agent's system prompt
- [ ] Create feedback collection template (see FEEDBACK_TEMPLATE.md)
- [ ] Set up monitoring dashboard
- [ ] Configure Telemetry endpoint
- [ ] Establish weekly sync schedule

## Example: Using with Claude

1. Copy content from any SYSTEM_PROMPT_*.md
2. When starting a conversation with Claude, paste at the beginning:

```
[SYSTEM PROMPT CONTENT HERE]

Now, here's my first requirement:
[YOUR REQUIREMENT]
```

Claude will then take on that agent role and respond accordingly.

## Tips

✅ Keep agent prompts focused and concise  
✅ Provide full context when switching between agents  
✅ Use output from one agent as input to next  
✅ Archive completed feedback regularly  
✅ Review Telemetry reports weekly  

---

**For more details on each agent, see the individual SYSTEM_PROMPT_*.md files.**
