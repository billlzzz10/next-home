# BL1NK Workspace Skills - Real Examples

Reference guide for the 10 skills identified in BL1NK workspace analysis.

## Phase 1: Critical Foundation Skills (Week 1, 5-8 hours)

### 1. text-processor (1-2 hours) - MISSING/RECOVERY
**Status**: Documented in analysis but missing implementation
**Purpose**: Process and analyze text with various operations
**Operations**:
- `count` - Count chars, words, lines, spaces
- `stats` - Word frequency, average length, unique words
- `reverse` - Reverse text
- `capitalize` - Title case text

**Input**: Text content + operation type
**Output**: Analyzed/transformed text
**Integration**: No external dependencies
**Example**: "Reverse this text" → reversing logic
**Best For**: Text transformation, quick analysis

---

### 2. log-analyzer (2-3 hours)
**Purpose**: Parse logs, extract patterns, filter by level
**Features**:
- Auto-detect log format (JSON, syslog, text)
- Filter by level (ERROR, WARNING, INFO, DEBUG)
- Group by timestamp/level/source
- Identify common error patterns

**Input**: Log content + filters
**Output**: Structured analysis with statistics
**Integration**: No external dependencies
**Best For**: Debugging, monitoring, troubleshooting

---

### 3. notification-router (2-3 hours)
**Purpose**: Route analysis results to notification channels
**Channels**: Slack, Linear, ClickUp
**Features**:
- Support for multiple channels simultaneously
- Error handling and retry logic
- Delivery status reporting

**Input**: Message + target channels + credentials
**Output**: Delivery report
**Integration**: Reuse `NotificationManager` from `/home/user/projects/bl1nk-architect/src/notifications/`
**Best For**: Workflow automation, team communication

---

## Phase 2: Integration-Enabled Skills (Week 2, 9-12 hours)

### 4. github-repo-analyzer (3-4 hours)
**Purpose**: Analyze GitHub repository health and structure
**Analyses**:
- Repository structure
- Code metrics (complexity, lines)
- Dependencies health
- CI/CD presence
- Overall health score

**Input**: GitHub repo URL + analysis type
**Output**: Structured health report
**Integration**: Use `GithubClient` from `/home/user/projects/bl1nk-architect/src/github_client.py`
**Best For**: Project assessment, code quality review

---

### 5. prompt-optimizer (2-3 hours)
**Purpose**: Optimize and refine LLM prompts
**Optimization Types**:
- `clarity` - Improve clarity and specificity
- `creativity` - Add flexibility and context
- `precision` - Add constraints and formats

**Input**: Prompt + target model + optimization type
**Output**: Optimized prompt + improvements list
**Integration**: Reference AI/LLM best practices
**Best For**: Improving AI prompt quality

---

### 6. poe-bot-generator (4-5 hours)
**Purpose**: Generate POE protocol-compliant bot implementations
**Features**:
- Scaffold FastAPI bot structure
- Implement POE protocol handlers
- Generate test curl commands
- Include requirements.txt

**Input**: Bot name + description + capabilities
**Output**: Complete bot code + tests
**Integration**: Reference POE protocol specs from `/home/user/docs/poe-protocol/`
**Best For**: Rapid POE bot development

---

## Phase 3: Platform Maturity Skills (Week 3-4, 10-13 hours)

### 7. code-analyzer (3-4 hours)
**Purpose**: Analyze code quality and complexity
**Analyses**:
- Cyclomatic complexity
- Code smells detection
- Performance anti-patterns
- Security issues

**Input**: Source code + language + analysis type
**Output**: Metrics + issues + recommendations
**Integration**: Use AST parsing for language analysis
**Best For**: Code review, quality improvement

---

### 8. skill-chain-executor (4-5 hours)
**Purpose**: Execute multiple skills in sequence with data flow
**Features**:
- Sequential skill execution
- Data passing between skills
- Error handling strategies
- Execution metrics

**Input**: Skill sequence + initial data + error strategy
**Output**: Results from each step + execution report
**Integration**: Use `SkillLoader` from `/home/user/projects/bl1nk-architect/src/skill_loader.py`
**Best For**: Complex multi-step workflows

---

### 9. document-generator (3-4 hours)
**Purpose**: Generate markdown documentation from code/specs
**Capabilities**:
- Code documentation extraction
- API docs generation
- Table of contents creation
- Template support

**Input**: Content + type + template
**Output**: Formatted markdown document
**Integration**: AST parsing for code analysis
**Best For**: Auto-documentation, API reference generation

---

## Phase 4: Advanced Capabilities (Backlog, 4-5 hours)

### 10. test-generator (4-5 hours)
**Purpose**: Generate unit tests from source code
**Features**:
- Automated test case generation
- Mock/stub creation
- Coverage estimation
- Multiple test frameworks

**Input**: Source code + language + framework
**Output**: Test code + coverage estimate
**Integration**: Test framework knowledge
**Best For**: Automated testing, coverage improvement

---

## Integration Dependencies Map

```
text-processor → No dependencies
log-analyzer → No dependencies
notification-router → NotificationManager (existing)
github-repo-analyzer → GithubClient (existing)
prompt-optimizer → LLM knowledge
poe-bot-generator → POE protocol specs
code-analyzer → AST parsing
skill-chain-executor → SkillLoader (existing)
document-generator → Template engine
test-generator → Test frameworks
```

---

## Common Characteristics

All BL1NK skills follow these patterns:

1. **JSON Input/Output**: All use stdin/stdout JSON
2. **Error Handling**: Graceful error messages
3. **Manifest Registration**: Updated in manifest.json
4. **Documentation**: Clear SKILL.md with examples
5. **Testing**: Provided test cases
6. **Integration**: Use existing code when possible

---

## When Creating a New Skill

1. **Identify Phase**: Which phase does it belong to?
2. **Check Examples**: Which existing skill is similar?
3. **Reuse Code**: Can you leverage existing integrations?
4. **Estimate Effort**: Based on similar skills
5. **Plan Integration**: What manifest.json entries needed?

