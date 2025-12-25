# 🔌 Integration Guide

## Method 1: Direct Claude Usage (No Setup)

**Simplest - Use immediately:**

1. Go to Claude.ai
2. Start new conversation
3. Copy entire `SYSTEM_PROMPT_PROJECT_MANAGER.md`
4. Paste as your first message
5. Then add your requirement

**Repeat for specialized agents:**
- Use the relevant SYSTEM_PROMPT for your need
- Paste its content first
- Then provide your task/requirement

---

## Method 2: API Integration

### OpenAI API + Python

```python
import openai

# Load agent prompt
with open("SYSTEM_PROMPT_PROJECT_MANAGER.md") as f:
    system_prompt = f.read()

# Create agent
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "Add dashboard feature to web app"}
    ]
)

print(response.choices[0].message.content)
```

### Anthropic Claude API

```python
from anthropic import Anthropic

with open("SYSTEM_PROMPT_PROJECT_MANAGER.md") as f:
    system_prompt = f.read()

client = Anthropic()
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=2048,
    system=system_prompt,
    messages=[
        {"role": "user", "content": "Add dashboard feature"}
    ]
)

print(response.content[0].text)
```

---

## Method 3: Multi-Agent Orchestration (Advanced)

### Using LangChain

```python
from langchain.chat_models import ChatOpenAI
from langchain.agents import Agent, AgentExecutor, tool
import os

# Initialize agents
agents = {}
agent_files = [
    "SYSTEM_PROMPT_PROJECT_MANAGER.md",
    "SYSTEM_PROMPT_ARCHITECTURE_DESIGNER.md",
    "SYSTEM_PROMPT_OAUTH_WORKSPACE.md",
    "SYSTEM_PROMPT_REVIEWER.md",
    "SYSTEM_PROMPT_DOCUMENT_WRITER.md",
    "SYSTEM_PROMPT_CICD_DEPLOYMENT.md",
    "SYSTEM_PROMPT_TELEMETRY_FEEDBACK.md"
]

for agent_file in agent_files:
    with open(agent_file) as f:
        prompt = f.read()
    
    agent_name = agent_file.replace("SYSTEM_PROMPT_", "").replace(".md", "")
    agents[agent_name] = ChatOpenAI(model="gpt-4", system_prompt=prompt)

# Usage
pm_response = agents["PROJECT_MANAGER"].predict(
    input="Add new Dashboard feature"
)
print(pm_response)
```

---

## Method 4: Webhook-Based (Discord/Slack)

### Discord Integration

```python
import discord
from discord.ext import commands

bot = commands.Bot()

# Load PM agent
with open("SYSTEM_PROMPT_PROJECT_MANAGER.md") as f:
    system_prompt = f.read()

@bot.command()
async def pm(ctx, *, requirement):
    """Project manager agent"""
    # Call your LLM with system_prompt
    response = call_agent(system_prompt, requirement)
    await ctx.send(response)

bot.run(TOKEN)
```

### N8N Workflow

```
1. Webhook (Discord/Slack input)
   ↓
2. HTTP Request (to Claude API)
   - Headers: Auth token
   - Body: { system: prompt, user_message: input }
   ↓
3. PM Agent processes
   ↓
4. Switch: Route to specialists based on PM output
   - Arch → Call Architecture Agent
   - Auth → Call OAuth Agent
   - etc.
   ↓
5. Aggregate Results
   ↓
6. Post back to Discord/Slack
```

---

## Method 5: GitHub Actions Pipeline

```yaml
name: Agent Workflow
on: [pull_request]

jobs:
  agent-review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run Agent Reviewer
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          python agent-reviewer.py ${{ github.event.pull_request.files }}
          
      - name: Comment on PR
        uses: actions/github-script@v6
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `Agent Review:\n${agentOutput}`
            })
```

---

## Method 6: Scheduled Reports

### Cron Job (Daily Telemetry)

```bash
#!/bin/bash
# /usr/local/bin/agent-telemetry.sh

# Run telemetry agent
python3 << 'PYTHON_EOF'
import anthropic
import json
from datetime import datetime

with open("/home/user/docs/agents/SYSTEM_PROMPT_TELEMETRY_FEEDBACK.md") as f:
    prompt = f.read()

client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=2048,
    system=prompt,
    messages=[{"role": "user", "content": "Daily summary of project telemetry"}]
)

# Log report
report = {
    "timestamp": datetime.now().isoformat(),
    "report": response.content[0].text
}

with open("/tmp/telemetry_report.json", "w") as f:
    json.dump(report, f, indent=2)

print("✅ Telemetry report saved")
PYTHON_EOF

# Post to your dashboard/Slack
curl -X POST https://slack.com/api/chat.postMessage \
  -H "Authorization: Bearer $SLACK_TOKEN" \
  -d "channel=project-updates" \
  -d "text=$(cat /tmp/telemetry_report.json)"
```

### Add to crontab
```bash
0 9 * * 1 /usr/local/bin/agent-telemetry.sh  # Daily at 9 AM Monday
```

---

## Testing Your Integration

### Test 1: Simple PM Agent

```bash
python3 << 'EOF'
import anthropic

with open("SYSTEM_PROMPT_PROJECT_MANAGER.md") as f:
    prompt = f.read()

client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    system=prompt,
    messages=[{
        "role": "user",
        "content": "I need to add a new API endpoint for user profiles"
    }]
)

print(response.content[0].text)
