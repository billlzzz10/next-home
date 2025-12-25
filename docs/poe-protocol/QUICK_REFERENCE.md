# Poe Protocol Quick Reference

## Minimal Working Example

```python
from flask import Flask, Response
import json
import os

app = Flask(__name__)

@app.route("/", methods=["POST"])
def bot():
    # Verify auth (hardcoded for demo)
    if request.headers.get("Authorization") != "Bearer your_key":
        return {"error": "Unauthorized"}, 401
    
    def stream():
        # Meta event (required)
        yield f'event: meta\ndata: {json.dumps({"content_type": "text/markdown"})}\n\n'
        
        # Text event(s)
        yield f'event: text\ndata: {json.dumps({"text": "Hello world!"})}\n\n'
        
        # Done event (required)
        yield f'event: done\ndata: {json.dumps({{}})}\n\n'
    
    return Response(stream(), mimetype="text/event-stream")

app.run(port=5000)
```

## Request Types at a Glance

### query (User sends message)
```json
{
  "type": "query",
  "version": "1.0",
  "message_id": "m-...",
  "user_id": "u-...",
  "conversation_id": "c-...",
  "query": [
    {"role": "system", "content": "system prompt"},
    {"role": "user", "content": "hello"}
  ]
}
```

### settings (Bot configuration)
```json
{"type": "settings"}
```
**Return**: HTTP 200 + JSON
```json
{
  "response_version": 1,
  "allow_attachments": true,
  "introduction_message": "Hi!"
}
```

### report_reaction (User likes/hearts message)
```json
{
  "type": "report_reaction",
  "message_id": "m-...",
  "reaction": "heart"
}
```

## Response Events

| Event | When | Required | Data |
|-------|------|----------|------|
| `meta` | First | Yes | `{"content_type": "text/markdown"}` |
| `text` | Content | Yes (≥1) | `{"text": "..."}` |
| `file` | Attachment | No | `{"url": "...", "name": "...", "content_type": "..."}` |
| `suggested_reply` | Suggestions | No | `{"text": "..."}` |
| `error` | Error occurred | No | `{"text": "msg", "allow_retry": true}` |
| `done` | End | Yes | `{}` |

## Quick Checklist

- [ ] POST to `/` endpoint
- [ ] Check `Authorization: Bearer KEY`
- [ ] Return 200 + SSE for `query`
- [ ] Return 200 + JSON for `settings`
- [ ] First event: `meta` with `content_type`
- [ ] Last event: `done`
- [ ] Response within 5s initially, 3600s total
- [ ] Response ≤ 512,000 chars
- [ ] Return 501 for unknown types

## Common Pitfalls

❌ Forgot `done` event  
❌ `meta` not first  
❌ Forgot `content_type` in meta  
❌ JSON syntax errors in event data  
❌ Took >5 seconds for first response  
❌ Didn't verify Authorization header  
❌ Returned 500 instead of streaming error event  

## Error Types

```
"insufficient_fund"      - User out of points
"user_message_too_long"  - Input too large
"user_caused_error"      - Invalid input/format
```

## Event Stream Format

```
event: type
data: {"field": "value"}

event: type
data: {"field": "value"}

```

✅ Always end with blank line after `data:`  
✅ Each event separated by blank line  
✅ Multi-line `data` indents continuation lines  
✅ `data:` value must be valid JSON  

## Testing

```bash
# Test settings
curl -X POST http://localhost:5000 \
  -H "Authorization: Bearer key123" \
  -H "Content-Type: application/json" \
  -d '{"type":"settings"}'

# Test query
curl -X POST http://localhost:5000 \
  -H "Authorization: Bearer key123" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "query",
    "version": "1.0",
    "message_id": "m-a1234567890123456789012345678901",
    "user_id": "u-a1234567890123456789012345678901",
    "conversation_id": "c-a1234567890123456789012345678901",
    "query": [{"role": "user", "content": "hi"}]
  }'
```

## ID Format

All identifiers match: `^[a-z]{1,3}-[a-z0-9=]{32}$`

**Types:**
- `m-` = message ID
- `u-` = user ID
- `c-` = conversation ID
- `d-` = metadata ID

## Parameter Hints (from query)

```json
{
  "temperature": 0.7,
  "skip_system_prompt": false,
  "stop_sequences": ["\n\n"],
  "logit_bias": {"token": 0.5}
}
```

These are optional hints. You can ignore them.

## Content Types

- `text/plain` - Plain text (no markdown)
- `text/markdown` - GitHub-Flavored Markdown

## Response Time Limits

- **Initial response**: ≤ 5 seconds
- **Total response**: ≤ 3600 seconds (1 hour)
- **Max response size**: 512,000 characters
- **Max events**: 10,000 events

## Key Settings

```json
{
  "response_version": 1,
  "allow_attachments": true,
  "expand_text_attachments": true,
  "enable_image_comprehension": false,
  "introduction_message": "Hello!",
  "server_bot_dependencies": {"Claude": 1},
  "enforce_author_role_alternation": false,
  "enable_multi_entity_prompting": false
}
```

## Deployment Checklist

- [ ] HTTPS (required in production)
- [ ] Verify Authorization header
- [ ] Stream SSE correctly
- [ ] Handle all request types
- [ ] Return appropriate HTTP status codes
- [ ] Log errors for debugging
- [ ] Set timeouts on external calls
- [ ] Rate limiting if needed
- [ ] Graceful error handling
- [ ] Monitor performance

## Links

- **Poe**: https://poe.com/
- **SSE Spec**: https://html.spec.whatwg.org/multipage/server-sent-events.html
- **GFM**: https://github.github.com/gfm/
- **SDK**: https://github.com/poe-platform/poe-python-api

