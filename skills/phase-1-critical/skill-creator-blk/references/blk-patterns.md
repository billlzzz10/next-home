# BL1NK Skill Patterns - Implementation Guide

Common patterns used across BL1NK skills organized by type.

## Pattern 1: Text/Data Processing

**Use When**: Processing text, analyzing data, transforming formats

**Characteristics**:
- Input: Text/data content + operation parameter
- Processing: Parse, transform, analyze
- Output: Results or transformed data
- Dependencies: None or minimal

**Examples**: text-processor, log-analyzer

**Structure**:
```python
#!/usr/bin/env python3
import json
import sys

data = json.loads(sys.stdin.read())
content = data.get('content', '')
operation = data.get('operation', 'default')

try:
    if operation == 'analyze':
        result = analyze(content)
    elif operation == 'transform':
        result = transform(content)
    
    output = {'status': 'success', 'result': result}
except Exception as e:
    output = {'status': 'error', 'message': str(e)}

print(json.dumps(output))
```

**Key Points**:
- Handle edge cases (empty input, invalid operations)
- Return structured JSON responses
- Include status field for error handling

---

## Pattern 2: External Integration

**Use When**: Interacting with external APIs (GitHub, Slack, etc.)

**Characteristics**:
- Input: Parameters + credentials/URLs
- Processing: Call external API
- Output: API results or status
- Dependencies: External client libraries

**Examples**: notification-router, github-repo-analyzer

**Structure**:
```python
#!/usr/bin/env python3
import json
import sys
from existing_client import ExternalClient

data = json.loads(sys.stdin.read())
api_key = data.get('api_key')
params = data.get('params', {})

try:
    client = ExternalClient(api_key=api_key)
    result = client.do_action(**params)
    output = {'status': 'success', 'result': result}
except Exception as e:
    output = {'status': 'error', 'message': str(e)}

print(json.dumps(output))
```

**Key Points**:
- Reuse existing client classes when available
- Handle auth/credentials safely
- Add retry logic for reliability
- Clear error messages

**BL1NK Integration Classes**:
```
NotificationManager → notification-router
GithubClient → github-repo-analyzer
GeminiClient → prompt-optimizer
SkillLoader → skill-chain-executor
```

---

## Pattern 3: Multi-Operation

**Use When**: Skill supports multiple different operations

**Characteristics**:
- Input: Content + operation type selector
- Processing: Execute based on operation
- Output: Operation-specific results
- Dependencies: Minimal

**Examples**: text-processor (count/stats/reverse/capitalize)

**Structure**:
```python
operations = {
    'operation1': handler_1,
    'operation2': handler_2,
    'operation3': handler_3,
}

operation = data.get('operation', 'default')
if operation not in operations:
    raise ValueError(f"Unknown operation: {operation}")

handler = operations[operation]
result = handler(content, params)
```

**Key Points**:
- Support default operation
- Validate operation name
- Document all operations in SKILL.md
- Each operation should have clear contract

---

## Pattern 4: Filtering & Grouping

**Use When**: Processing collections with filters/grouping

**Characteristics**:
- Input: Data + filter criteria + grouping
- Processing: Filter, group, aggregate
- Output: Organized results with statistics
- Dependencies: Minimal

**Examples**: log-analyzer

**Structure**:
```python
def filter_and_group(items, filter_spec, group_by):
    filtered = [i for i in items if matches_filter(i, filter_spec)]
    grouped = group_items(filtered, group_by)
    stats = calculate_statistics(grouped)
    return {'grouped': grouped, 'stats': stats}
```

**Key Points**:
- Make filters optional
- Support multiple grouping options
- Return both raw data and statistics
- Document filter syntax clearly

---

## Pattern 5: POE Protocol Compliance

**Use When**: Creating POE bots or analyzing POE

**Characteristics**:
- Framework: FastAPI + fastapi_poe
- Input: POE protocol QueryRequest
- Output: SSE event stream
- Dependencies: fastapi_poe library

**Example**: poe-bot-generator

**Structure**:
```python
import fastapi_poe as fp
from fastapi import FastAPI

app = FastAPI()

class MyBot(fp.PoeBot):
    async def get_response(self, request: fp.QueryRequest):
        yield fp.MetaResponse(content_type="text/markdown")
        
        # Process query
        user_message = request.query[-1].content
        response = process_message(user_message)
        
        yield fp.PartialResponse(text=response)
        yield fp.done_response()

# Register with POE
@app.post("/")
async def bot_handler(request: fp.QueryRequest):
    return await MyBot().handle_request(request)
```

**Key Points**:
- Use MetaResponse with content_type
- Stream responses with PartialResponse
- End with done event
- Handle errors with ErrorResponse

**Reference**: `/home/user/docs/poe-protocol/`

---

## Pattern 6: Orchestration & Chaining

**Use When**: Coordinating multiple skills or complex workflows

**Characteristics**:
- Input: Skill list + data + error strategy
- Processing: Execute sequentially, pass data
- Output: Aggregated results
- Dependencies: SkillLoader

**Example**: skill-chain-executor

**Structure**:
```python
from skill_loader import SkillLoader

def execute_chain(skills, initial_data, error_handling='stop'):
    results = []
    current_data = initial_data
    
    for skill_name in skills:
        try:
            skill = SkillLoader.load(skill_name)
            result = skill.execute(current_data)
            results.append(result)
            current_data = result.output  # Data flows to next
        except Exception as e:
            if error_handling == 'stop':
                raise
            elif error_handling == 'continue':
                results.append({'error': str(e)})
    
    return results
```

**Key Points**:
- Load skills dynamically
- Pass output from one skill to next
- Support different error strategies
- Track execution metrics

---

## Pattern 7: Template/Boilerplate Generation

**Use When**: Generating code, documents, or configurations

**Characteristics**:
- Input: Parameters + template selections
- Processing: Fill templates with values
- Output: Generated content
- Dependencies: Template engine

**Example**: poe-bot-generator, frontend-design

**Structure**:
```python
def generate_from_template(template_name, params):
    template = load_template(template_name)
    # Validate params against template requirements
    validate_params(template, params)
    # Render with parameters
    result = template.render(**params)
    return result
```

**Key Points**:
- Store templates in `assets/`
- Validate all parameters upfront
- Include example output
- Document all template variables

---

## Common I/O Patterns

### Standard JSON Input Format
```json
{
  "param1": "value",
  "param2": {
    "nested": "data"
  },
  "operation": "operation_name"
}
```

### Standard JSON Output Format
```json
{
  "status": "success|error",
  "result": {},
  "message": "optional error message",
  "metadata": {
    "execution_time": 0.123,
    "version": "1.0.0"
  }
}
```

### Error Response Format
```json
{
  "status": "error",
  "message": "Human-readable error message",
  "code": "ERROR_CODE",
  "details": {
    "parameter": "which parameter had the issue",
    "reason": "why it's invalid"
  }
}
```

---

## SKILL.md Frontmatter Pattern

```yaml
---
name: skill-name
description: |
  What the skill does and when to use it.
  Include:
  1. Primary use case
  2. Secondary use cases (if any)
  3. When NOT to use
  4. Integration points
license: Complete terms in LICENSE.txt
---
```

---

## Testing Pattern

Every skill should include test cases in SKILL.md:

```markdown
## Testing

### Test 1: Basic Operation
Input:
```json
{"param": "value", "operation": "basic"}
```
Expected: Successful execution

### Test 2: Error Handling
Input:
```json
{"param": "", "operation": "invalid"}
```
Expected: Error with clear message
```

---

## Integration References

When using external services:

**Notifications**:
- File: `/home/user/projects/bl1nk-architect/src/notifications/notification_manager.py`
- Classes: NotificationManager, SlackNotifier, LinearNotifier, ClickUpNotifier

**GitHub**:
- File: `/home/user/projects/bl1nk-architect/src/github_client.py`
- Class: GithubClient

**POE Protocol**:
- Docs: `/home/user/docs/poe-protocol/`
- Key file: `POE_PROTOCOL_SPEC.md`
- Library: `fastapi_poe`

**Skill Loader**:
- File: `/home/user/projects/bl1nk-architect/src/skill_loader.py`
- Class: SkillLoader

