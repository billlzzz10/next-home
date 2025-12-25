# ✅ SKILLS IMPLEMENTATION CHECKLIST

## Overview
This checklist guides the creation of 10 new skills + 1 recovery.
Each section corresponds to one skill with specific tasks and validation steps.

---

## 🔴 PHASE 1: Recovery & Critical Fixes (Week 1)

### Task 1.1: text-processor (URGENT - MISSING)

**Status:** ❌ MISSING (Referenced in manifest but no implementation)

#### File Setup
- [ ] Create `/home/user/skills/text-processor/` directory
- [ ] Create `/home/user/skills/text-processor/SKILL.md`
- [ ] Create `/home/user/skills/text-processor/scripts/` directory
- [ ] Create `/home/user/skills/text-processor/scripts/run.py`
- [ ] Create `/home/user/skills/text-processor/examples/` directory

#### Implementation
- [ ] Copy SKILL.md template from blueprint
  - Fill in all metadata fields
  - Define 4 operations: count, stats, reverse, capitalize
  - Specify inputs/outputs correctly
  
- [ ] Implement scripts/run.py
  - [ ] Accept JSON input from stdin
  - [ ] Parse text and operation parameters
  - [ ] Implement count operation (chars, words, lines, spaces)
  - [ ] Implement stats operation (word frequency, avg length, unique words)
  - [ ] Implement reverse operation (reverse entire text)
  - [ ] Implement capitalize operation (title case)
  - [ ] Return JSON output with status and results

#### Testing
- [ ] Test count operation
  ```bash
  echo '{"text": "Hello World", "operation": "count"}' | python scripts/run.py
  # Expected: {"status": "success", "operation": "count", "result": {"total_chars": 11, "total_words": 2, ...}}
  ```

- [ ] Test stats operation
  ```bash
  echo '{"text": "The quick brown fox", "operation": "stats"}' | python scripts/run.py
  # Expected: word frequency analysis
  ```

- [ ] Test reverse operation
  ```bash
  echo '{"text": "Hello", "operation": "reverse"}' | python scripts/run.py
  # Expected: {"reversed_text": "olleH"}
  ```

- [ ] Test capitalize operation
  ```bash
  echo '{"text": "hello world", "operation": "capitalize"}' | python scripts/run.py
  # Expected: {"capitalized_text": "Hello World"}
  ```

- [ ] Test invalid operation (error handling)
- [ ] Test empty text input
- [ ] Test default operation (should use 'count')

#### Documentation
- [ ] Create examples/input_count.json
- [ ] Create examples/output_count.json
- [ ] Create examples/input_stats.json
- [ ] Create examples/output_stats.json
- [ ] Add usage examples to SKILL.md

#### Integration
- [ ] Update `/home/user/skills/skills.json` with text-processor entry
- [ ] Update `/home/user/skills/manifest.json` with full metadata
- [ ] Update `/home/user/skills/README.md` with text-processor documentation
- [ ] Verify no conflicts with other skills

#### Validation
- [ ] Run complete test suite
- [ ] Verify skill loads without errors
- [ ] Check JSON output is valid
- [ ] Ensure all 4 operations work correctly

**Time Estimate:** 1-2 hours

---

### Task 1.2: log-analyzer

**Status:** 🟠 NEW (Ready to implement)

#### File Setup
- [ ] Create `/home/user/skills/log-analyzer/` directory
- [ ] Create `/home/user/skills/log-analyzer/SKILL.md`
- [ ] Create `/home/user/skills/log-analyzer/scripts/run.py`
- [ ] Create `/home/user/skills/log-analyzer/examples/` directory
- [ ] Create `/home/user/skills/log-analyzer/scripts/log_parser.py` (helper)

#### Implementation
- [ ] Create SKILL.md with:
  - [ ] Metadata and description
  - [ ] 3 input parameters: log_content, filter_level, group_by
  - [ ] 4 output fields: total_entries, entries_by_level, summary, patterns_found

- [ ] Implement scripts/log_parser.py helper
  - [ ] Auto-detect log format (JSON, syslog, text)
  - [ ] Parse timestamps
  - [ ] Extract log levels (ERROR, WARNING, INFO, DEBUG)
  - [ ] Identify common patterns (connection errors, timeouts, etc.)

- [ ] Implement scripts/run.py
  - [ ] Read log content from input
  - [ ] Apply filter_level filter
  - [ ] Group by specified dimension
  - [ ] Calculate statistics
  - [ ] Return structured analysis

#### Testing
- [ ] Create test log file (example errors, warnings, info)
- [ ] Test with filter_level="error"
- [ ] Test with group_by="level"
- [ ] Test with group_by="timestamp"
- [ ] Test pattern detection (common errors)
- [ ] Test edge cases (empty logs, malformed entries)

#### Documentation
- [ ] Create examples with sample logs
- [ ] Document supported log formats
- [ ] Add troubleshooting tips in SKILL.md

#### Integration
- [ ] Update manifest.json and skills.json

**Time Estimate:** 2-3 hours

---

### Task 1.3: notification-router

**Status:** 🟡 PARTIAL (Code exists, needs wrapping)

#### File Setup
- [ ] Create `/home/user/skills/notification-router/` directory
- [ ] Create `/home/user/skills/notification-router/SKILL.md`
- [ ] Create `/home/user/skills/notification-router/scripts/run.py`
- [ ] Create `/home/user/skills/notification-router/examples/` directory

#### Implementation
- [ ] Create SKILL.md
  - [ ] Define message object structure
  - [ ] List supported channels: slack, linear, clickup
  - [ ] Specify webhook_urls object format

- [ ] Implement scripts/run.py
  - [ ] Import NotificationManager from bl1nk-architect
  - [ ] Parse input: message, channels, webhook_urls
  - [ ] Route to each channel
  - [ ] Collect delivery results
  - [ ] Return success/failure report

- [ ] Handle credentials
  - [ ] Load from environment variables (SLACK_WEBHOOK, LINEAR_API_KEY, etc.)
  - [ ] Accept credentials in input (fallback)
  - [ ] Log but don't expose sensitive data

#### Testing
- [ ] Test with mock webhook URLs
- [ ] Test single channel (Slack only)
- [ ] Test multiple channels
- [ ] Test missing credentials (should fail gracefully)
- [ ] Test malformed message object

#### Documentation
- [ ] Add example payloads for each channel
- [ ] Document channel-specific message formats
- [ ] Include environment variable requirements

#### Integration
- [ ] Update manifest and skills.json

**Time Estimate:** 2-3 hours

**Phase 1 Total:** 5-8 hours

---

## 🟠 PHASE 2: Integration Enablement (Week 2)

### Task 2.1: github-repo-analyzer

**Status:** 🟡 NEW

#### File Setup
- [ ] Create `/home/user/skills/github-repo-analyzer/` directory
- [ ] Create SKILL.md and scripts/run.py
- [ ] Create helper scripts for analysis

#### Implementation
- [ ] Implement structure analysis
  - [ ] Parse README existence
  - [ ] Count code files by type
  - [ ] Detect CI/CD files
  - [ ] Check test coverage structure

- [ ] Implement health scoring
  - [ ] README presence (20%)
  - [ ] Tests exist (20%)
  - [ ] CI/CD config (20%)
  - [ ] Documentation (20%)
  - [ ] License file (10%)
  - [ ] Code organization (10%)

- [ ] Use existing github_client.py
  - [ ] Import GithubClient
  - [ ] Parse repo URL
  - [ ] Fetch repo metadata

#### Testing
- [ ] Test with public repo
- [ ] Test structure analysis
- [ ] Test health scoring
- [ ] Test with private repo (if token provided)

**Time Estimate:** 3-4 hours

---

### Task 2.2: prompt-optimizer

**Status:** 🟡 NEW

#### Implementation
- [ ] Create optimization rules
  - [ ] Clarity: Add specific instructions
  - [ ] Creativity: Remove constraints, add context
  - [ ] Precision: Add output format specs

- [ ] Implement prompt scoring
  - [ ] Clarity score
  - [ ] Specificity score
  - [ ] Format score
  - [ ] Context score

- [ ] Generate improvements
  - [ ] List of 3-5 suggested improvements
  - [ ] Before/after comparison

#### Testing
- [ ] Test with vague prompt
- [ ] Test with well-written prompt
- [ ] Test all optimization types

**Time Estimate:** 2-3 hours

---

### Task 2.3: poe-bot-generator

**Status:** 🟡 NEW

#### Implementation
- [ ] Create bot code templates
  - [ ] FastAPI skeleton
  - [ ] POE protocol handlers
  - [ ] Settings endpoint
  - [ ] Query handler with SSE
  - [ ] Error handling

- [ ] Generate test curl commands
  - [ ] Settings test
  - [ ] Query test
  - [ ] Error test

- [ ] Include requirements.txt generation
  - [ ] fastapi, uvicorn
  - [ ] fastapi-poe
  - [ ] Other common deps

#### Testing
- [ ] Generate bot code
- [ ] Verify syntax
- [ ] Test generated curl commands work
- [ ] Test all response formats (text, markdown, html)

**Time Estimate:** 4-5 hours

**Phase 2 Total:** 9-12 hours

---

## 🟡 PHASE 3: Platform Maturity (Week 3-4)

### Task 3.1: code-analyzer

**Time Estimate:** 3-4 hours

Tasks:
- [ ] Implement AST parsing
- [ ] Calculate cyclomatic complexity
- [ ] Detect code smells
- [ ] Generate quality score
- [ ] Support Python, JavaScript, TypeScript, Bash

---

### Task 3.2: skill-chain-executor

**Time Estimate:** 4-5 hours

Tasks:
- [ ] Load skills dynamically
- [ ] Execute sequentially
- [ ] Pass data between skills
- [ ] Implement error handling strategies
- [ ] Track execution metrics

---

### Task 3.3: document-generator

**Time Estimate:** 3-4 hours

Tasks:
- [ ] Parse source code/specs
- [ ] Generate Markdown
- [ ] Create table of contents
- [ ] Support multiple templates
- [ ] Generate API docs from code

**Phase 3 Total:** 10-13 hours

---

## 🟢 PHASE 4: Advanced (Backlog)

### Task 4.1: test-generator

**Time Estimate:** 4-5 hours

Tasks:
- [ ] Parse functions
- [ ] Generate test cases
- [ ] Create mocks/stubs
- [ ] Estimate coverage
- [ ] Support pytest, unittest, jest

---

## 📊 SUMMARY CHECKLIST

### Pre-Implementation
- [ ] Review all SKILL.md templates
- [ ] Understand workspace structure
- [ ] Set up development environment
- [ ] Read POE Protocol spec (if POE-related skill)

### Per-Skill
- [ ] Create directory structure
- [ ] Implement SKILL.md
- [ ] Implement scripts
- [ ] Create test cases
- [ ] Document examples
- [ ] Update manifest/skills.json
- [ ] Final validation

### Post-Implementation
- [ ] Update skills/README.md
- [ ] Create any necessary dependencies
- [ ] Test skill chaining (for orchestration skills)
- [ ] Performance benchmarking
- [ ] Documentation review

---

## 🔗 DEPENDENCY MAP

```
text-processor
  ↓ (no dependencies)

log-analyzer
  ↓ (no external dependencies)

notification-router
  ↓ Depends on: NotificationManager from bl1nk-architect
  ├─ SlackNotifier
  ├─ LinearNotifier
  └─ ClickUpNotifier

github-repo-analyzer
  ↓ Depends on: GithubClient from bl1nk-architect

prompt-optimizer
  ↓ Depends on: GeminiClient (optional)

poe-bot-generator
  ↓ Depends on: POE Protocol spec

code-analyzer
  ↓ (Uses stdlib AST module)

skill-chain-executor
  ↓ Depends on: SkillLoader, other skills

document-generator
  ↓ (No external dependencies)

test-generator
  ↓ (Uses stdlib)
```

---

## 📈 EFFORT TRACKING

| Phase | Tasks | Total Hours | Start | End |
|-------|-------|------------|-------|-----|
| Phase 1 | 3 skills | 5-8h | Week 1 Mon | Week 1 Thu |
| Phase 2 | 3 skills | 9-12h | Week 2 Mon | Week 2 Fri |
| Phase 3 | 3 skills | 10-13h | Week 3 Mon | Week 4 Fri |
| Phase 4 | 1 skill | 4-5h | Backlog | TBD |
| **Total** | **10 skills** | **28-38h** | | |

---

## ✨ SUCCESS CRITERIA

For each skill:
- [ ] All test cases pass
- [ ] JSON input/output valid
- [ ] Error handling works
- [ ] Documentation complete
- [ ] Examples provided
- [ ] No dependencies broken
- [ ] Code review passed

For entire project:
- [ ] All 10 skills implemented
- [ ] Manifest updated
- [ ] Skills load without errors
- [ ] Orchestration works
- [ ] 95% tests passing
- [ ] Documentation current

