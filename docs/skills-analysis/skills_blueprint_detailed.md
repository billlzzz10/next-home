# 📐 SKILLS BLUEPRINT - Detailed Specifications

---

## 🔴 CRITICAL: Phase 1 - Recovery & Essentials

### Skill #1: text-processor (⚡ MISSING - URGENT)

**File Location:** `/home/user/skills/text-processor/`

**SKILL.md Template:**
```yaml
---
name: text-processor
description: Analyze and process text with various operations
version: 1.0.0
author: BL1NK Team
tags: [text, analysis, transform, utility]
timeout: 30
entrypoint: scripts/run.py
interpreter: python
inputs:
  text:
    type: string
    description: Text content to process
    required: true
  operation:
    type: string
    description: Operation to perform (count|stats|reverse|capitalize)
    default: count
outputs:
  result:
    type: object
  operation_type:
    type: string
---
```

**Operations Specification:**
| Operation | Input | Output | Example |
|-----------|-------|--------|---------|
| count | text string | total_chars, total_words, lines | `{"total_chars": 50, "total_words": 10, "lines": 3}` |
| stats | text string | word_freq, avg_length, unique_words | `{"word_freq": {...}, "avg_word_length": 4.5, "unique": 8}` |
| reverse | text string | reversed_text | `{"reversed_text": "dlrow olleH"}` |
| capitalize | text string | capitalized_text | `{"capitalized_text": "Hello World"}` |

**Implementation Location:** `scripts/run.py`
```python
#!/usr/bin/env python3
import json
import sys
from collections import Counter

data = json.loads(sys.stdin.read())
text = data.get('text', '')
operation = data.get('operation', 'count').lower()

result = {}

if operation == 'count':
    result = {
        'total_chars': len(text),
        'total_words': len(text.split()),
        'lines': len(text.split('\n')),
        'total_spaces': text.count(' ')
    }
elif operation == 'stats':
    words = text.split()
    word_freq = Counter(words)
    avg_length = sum(len(w) for w in words) / len(words) if words else 0
    result = {
        'word_frequency': dict(word_freq.most_common(10)),
        'avg_word_length': round(avg_length, 2),
        'unique_words': len(set(words)),
        'total_words': len(words)
    }
elif operation == 'reverse':
    result = {'reversed_text': text[::-1]}
elif operation == 'capitalize':
    result = {'capitalized_text': text.title()}
else:
    raise ValueError(f"Unknown operation: {operation}")

print(json.dumps({'status': 'success', 'operation': operation, 'result': result}))
```

**Testing:**
```bash
# Test count
echo '{"text": "Hello World", "operation": "count"}' | python3 scripts/run.py

# Test stats
echo '{"text": "The quick brown fox jumps over the lazy dog", "operation": "stats"}' | python3 scripts/run.py

# Test reverse
echo '{"text": "Hello World", "operation": "reverse"}' | python3 scripts/run.py
```

---

### Skill #2: log-analyzer

**File Location:** `/home/user/skills/log-analyzer/`

**Purpose:** Parse application logs, extract patterns, filter by level, group entries

**SKILL.md:**
```yaml
---
name: log-analyzer
description: Parse and analyze log files with pattern matching and statistics
version: 1.0.0
author: BL1NK Team
tags: [logs, analysis, debugging, monitoring]
timeout: 60
entrypoint: scripts/run.py
interpreter: python
inputs:
  log_content:
    type: string
    description: Raw log text to analyze
    required: true
  filter_level:
    type: string
    description: Filter by log level (error|warning|info|debug|all)
    default: all
  group_by:
    type: string
    description: Group results by (timestamp|level|source|none)
    default: level
outputs:
  total_entries:
    type: integer
  entries_by_level:
    type: object
  summary:
    type: string
  patterns_found:
    type: array
---
```

**Features:**
- Auto-detect log format (JSON, syslog, custom)
- Extract severity levels
- Find common error patterns
- Group and summarize
- Suggest fixes for common errors

**Implementation hints:**
- Use regex for pattern detection
- Support multiple log formats
- Return structured analysis
- Include error frequency statistics

---

### Skill #3: notification-router

**File Location:** `/home/user/skills/notification-router/`

**Purpose:** Route messages to Slack, Linear, ClickUp using existing notification_manager.py

**SKILL.md:**
```yaml
---
name: notification-router
description: Route analysis results to Slack, Linear, ClickUp notification channels
version: 1.0.0
author: BL1NK Team
tags: [notifications, integration, workflow]
timeout: 45
entrypoint: scripts/run.py
interpreter: python
inputs:
  message:
    type: object
    description: Message content (title, body, priority)
    required: true
  channels:
    type: array
    description: Target channels (slack|linear|clickup)
    default: [slack]
  webhook_urls:
    type: object
    description: Channel-specific webhook URLs
    required: true
outputs:
  sent_to:
    type: array
    description: Successfully delivered channels
  failed:
    type: array
    description: Failed channels with error reasons
  delivery_status:
    type: string
---
```

**Integration with existing code:**
- Import NotificationManager from `/home/user/projects/bl1nk-architect/src/notifications/notification_manager.py`
- Use SlackNotifier, LinearNotifier, ClickUpNotifier classes
- Handle auth tokens from environment variables
- Return structured delivery report

---

## 🟠 Priority 2: Integration Enablement

### Skill #4: github-repo-analyzer

**SKILL.md:**
```yaml
---
name: github-repo-analyzer
description: Analyze GitHub repository structure, health, and statistics
version: 1.0.0
author: BL1NK Team
tags: [github, analysis, repository, assessment]
timeout: 120
entrypoint: scripts/run.py
interpreter: python
inputs:
  repo_url:
    type: string
    description: GitHub repository URL
    required: true
  analyze_type:
    type: string
    description: Analysis type (structure|health|dependencies|size|all)
    default: all
  token:
    type: string
    description: GitHub API token (optional, for private repos)
outputs:
  structure:
    type: object
  metrics:
    type: object
  health_score:
    type: number
  recommendations:
    type: array
---
```

**Analysis Dimensions:**
- File structure and organization
- Code metrics (lines, complexity)
- Dependency analysis
- Repository health (README, tests, CI/CD)
- License and documentation quality

---

### Skill #5: prompt-optimizer

**SKILL.md:**
```yaml
---
name: prompt-optimizer
description: Optimize and refine LLM prompts for better results
version: 1.0.0
author: BL1NK Team
tags: [ai, prompts, optimization, llm]
timeout: 30
entrypoint: scripts/run.py
interpreter: python
inputs:
  prompt:
    type: string
    description: Original prompt text
    required: true
  target_model:
    type: string
    description: Target AI model (gpt-4|claude|gemini|llama)
    default: gpt-4
  optimization_type:
    type: string
    description: Optimization strategy (clarity|creativity|precision)
    default: precision
outputs:
  optimized_prompt:
    type: string
  improvements:
    type: array
  score_before:
    type: number
  score_after:
    type: number
---
```

**Optimization Techniques:**
- Add specific instructions and constraints
- Improve clarity and reduce ambiguity
- Add relevant context
- Include output format specifications
- Suggest few-shot examples

---

### Skill #6: poe-bot-generator

**SKILL.md:**
```yaml
---
name: poe-bot-generator
description: Generate POE protocol-compliant bot implementations
version: 1.0.0
author: BL1NK Team
tags: [poe, bot, generator, automation]
timeout: 60
entrypoint: scripts/run.py
interpreter: python
inputs:
  bot_name:
    type: string
    description: Bot name
    required: true
  bot_description:
    type: string
    description: Bot purpose and behavior
    required: true
  capabilities:
    type: array
    description: Bot capabilities (query|settings|report_reaction)
    default: [query, settings]
  response_format:
    type: string
    description: Response format (text|markdown|html)
    default: markdown
outputs:
  bot_code:
    type: string
  requirements:
    type: array
  test_curl_commands:
    type: array
  deployment_guide:
    type: string
---
```

**Code Generation:**
- Generate FastAPI app with POE protocol handlers
- Include proper SSE streaming implementation
- Add error handling and validation
- Generate example test curl commands
- Include requirements.txt

---

## 🟡 Priority 3: Platform Maturity

### Skill #7: code-analyzer

**SKILL.md:**
```yaml
---
name: code-analyzer
description: Analyze code quality, complexity, and patterns
version: 1.0.0
author: BL1NK Team
tags: [code, quality, analysis, metrics]
timeout: 45
entrypoint: scripts/run.py
interpreter: python
inputs:
  code_content:
    type: string
    description: Source code to analyze
    required: true
  language:
    type: string
    description: Programming language (python|javascript|typescript|bash)
    default: python
  analysis_type:
    type: string
    description: Type of analysis (complexity|security|style|performance|all)
    default: all
outputs:
  metrics:
    type: object
  issues:
    type: array
  recommendations:
    type: array
  quality_score:
    type: number
---
```

**Metrics Covered:**
- Lines of code, cyclomatic complexity
- Function/variable naming conventions
- Dead code detection
- Security vulnerabilities
- Performance anti-patterns

---

### Skill #8: skill-chain-executor

**SKILL.md:**
```yaml
---
name: skill-chain-executor
description: Chain multiple skills together with data flow
version: 1.0.0
author: BL1NK Team
tags: [workflow, orchestration, skills, automation]
timeout: 300
entrypoint: scripts/run.py
interpreter: python
inputs:
  skill_sequence:
    type: array
    description: List of skill names to execute in order
    required: true
  initial_data:
    type: object
    description: Input data for first skill
    required: true
  error_handling:
    type: string
    description: Error strategy (stop|continue|rollback)
    default: stop
outputs:
  results:
    type: array
  execution_time:
    type: number
  status:
    type: string
---
```

**Features:**
- Sequential execution of skills
- Data flow between skills
- Conditional branching
- Error recovery
- Execution logging and metrics

---

### Skill #9: document-generator

**SKILL.md:**
```yaml
---
name: document-generator
description: Generate markdown documentation from code, specs, templates
version: 1.0.0
author: BL1NK Team
tags: [documentation, generator, markdown, api-docs]
timeout: 60
entrypoint: scripts/run.py
interpreter: python
inputs:
  content_type:
    type: string
    description: Type of content (code|spec|template|readme)
    required: true
  content:
    type: string
    description: Source content
    required: true
  template:
    type: string
    description: Documentation template format
    default: standard
outputs:
  markdown_doc:
    type: string
  toc:
    type: array
  metadata:
    type: object
---
```

**Documentation Types:**
- API documentation from code
- Architecture diagrams in Mermaid
- README generation
- API spec to docs
- Code comments extraction

---

### Skill #10: test-generator

**SKILL.md:**
```yaml
---
name: test-generator
description: Generate unit tests from source code
version: 1.0.0
author: BL1NK Team
tags: [testing, quality, automation, coverage]
timeout: 60
entrypoint: scripts/run.py
interpreter: python
inputs:
  source_code:
    type: string
    description: Source code to generate tests for
    required: true
  language:
    type: string
    description: Programming language (python|javascript|typescript)
    required: true
  test_framework:
    type: string
    description: Test framework (pytest|unittest|jest|mocha)
    default: pytest
outputs:
  test_code:
    type: string
  coverage_estimate:
    type: number
  test_cases:
    type: integer
---
```

**Test Generation:**
- Unit test structure
- Mock/stub generation
- Edge case identification
- Assertion generation
- Coverage estimation

---

## 📋 Universal SKILL.md Structure

Every skill must follow this structure:

```yaml
---
name: skill-name                          # Unique identifier
description: Short description            # 1 sentence
version: 1.0.0                           # Semantic versioning
author: BL1NK Team                        # Creator/team
tags: [tag1, tag2, tag3]                 # Categorization
timeout: 30                               # Max execution time (seconds)
entrypoint: scripts/run.py                # Entry script path
interpreter: python                      # python|bash|node
inputs:
  param_name:
    type: string|object|array|integer     # JSON type
    description: What this parameter does # Clear description
    required: true|false                  # Mandatory or optional
    default: value                        # Default value (if not required)
outputs:
  output_name:
    type: string|object|array|integer     # JSON type
  # Multiple outputs allowed
---

# Skill Name

Description and usage documentation.

## Operations
- **op1**: Description
- **op2**: Description

## Examples
```
```

## Troubleshooting
Common issues and solutions.
```

---

## 📂 File Structure for Each Skill

```
skills/
└── skill-namespace/
    └── skill-name/
        ├── SKILL.md                      # Metadata (required)
        ├── scripts/
        │   ├── run.py                    # Main entry point
        │   ├── requirements.txt          # Python dependencies (if needed)
        │   └── helpers.py                # Shared utilities (optional)
        ├── examples/
        │   ├── input.json                # Sample input
        │   └── output.json               # Expected output
        └── README.md                     # Extended documentation (optional)
```

---

## ✅ Checklist for Each Skill

- [ ] Create skill directory
- [ ] Write SKILL.md with complete frontmatter
- [ ] Create scripts/ directory
- [ ] Implement run.py/run.sh with proper JSON I/O
- [ ] Add requirements.txt (if needed)
- [ ] Create examples/ with input/output samples
- [ ] Test with: `echo '{}' | python scripts/run.py`
- [ ] Add to manifest.json
- [ ] Document in skills/README.md
- [ ] Add 2-3 usage examples in SKILL.md

---

## 🔗 Integration Points with Existing Code

**text-processor:**
- Uses: String processing utilities
- Integrates: utilities/formatter.py

**log-analyzer:**
- Uses: health_check.py for log format patterns
- Integrates: Logging infrastructure

**notification-router:**
- Uses: NotificationManager, SlackNotifier, LinearNotifier, ClickUpNotifier
- Location: src/notifications/*.py

**github-repo-analyzer:**
- Uses: GithubClient
- Location: src/github_client.py

**prompt-optimizer:**
- Uses: GeminiClient
- Location: src/gemini_client.py

**poe-bot-generator:**
- Uses: POE Protocol specs
- Reference: docs/poe-protocol/POE_PROTOCOL_SPEC.md

**code-analyzer:**
- Uses: AST parsing, pattern matching
- Reference: src/orchestrator.py

**skill-chain-executor:**
- Uses: SkillLoader, orchestrator logic
- Location: src/skill_loader.py

**document-generator:**
- Uses: Markdown generation, AST parsing
- Reference: 7 agent system prompts

**test-generator:**
- Uses: Code analysis, test templates
- Reference: tests/ directory

---

