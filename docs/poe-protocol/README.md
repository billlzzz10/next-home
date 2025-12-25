# Poe Protocol Documentation

Complete reference documentation for building custom bots on the Poe platform.

## 📚 Documents

### 1. **POE_PROTOCOL_SPEC.md** (Full Specification)
Comprehensive technical specification covering:
- Protocol introduction and architecture
- Core concepts (identifiers, authentication, versioning)
- All request types (`query`, `settings`, `report_reaction`, `report_error`)
- Response format and server-sent events
- Error handling with error types
- Implementation guide with Flask example
- Advanced topics (bot dependencies, parameter controls, attachments, metadata)

**Use this when:** You need complete protocol details, understanding how everything works together, or implementing a complex bot.

---

### 2. **QUICK_REFERENCE.md** (Cheat Sheet)
Quick lookup guide with:
- Minimal working example (5-line bot)
- Request types at a glance
- Response events table
- Common pitfalls and mistakes
- Testing commands with curl
- Deployment checklist

**Use this when:** You want quick lookups, need to remember format details, or troubleshooting common issues.

---

### 3. **IMPLEMENTATION_EXAMPLES.md** (Code Examples)
7 complete, production-ready examples:
1. **Echo Bot** - Simplest possible bot
2. **Streaming Bot** - Progressive word-by-word response
3. **Calculator Bot** - Expression parsing and evaluation
4. **Multi-Bot Orchestrator** - Coordinating multiple bots
5. **File Upload Handler** - Processing attachments
6. **Error Handling** - Proper error responses
7. **Suggested Replies** - Follow-up suggestions

**Use this when:** You're building a specific type of bot, need working code, or want to understand patterns.

---

## 🚀 Getting Started

### For Complete Beginners
1. Start with **QUICK_REFERENCE.md** → minimal example
2. Run one of the examples from **IMPLEMENTATION_EXAMPLES.md**
3. Test with curl commands
4. Refer to **POE_PROTOCOL_SPEC.md** for details

### For Experienced Developers
1. Scan **QUICK_REFERENCE.md** for format
2. Jump to relevant example in **IMPLEMENTATION_EXAMPLES.md**
3. Use **POE_PROTOCOL_SPEC.md** as reference

---

## 📋 Key Concepts At a Glance

### Request/Response Flow

```
User Input
    ↓
[Poe Server]
    ↓
POST to your bot server
    ↓
Your handler receives query
    ↓
Stream SSE events:
  1. meta (config)
  2. text (content)
  3. done (finish)
    ↓
[Poe Server] streams to user
```

### The Minimal Bot

Every bot needs:

1. **HTTP Endpoint**: `POST /` that accepts JSON
2. **Authentication**: Check `Authorization: Bearer KEY`
3. **Request Handling**: Dispatch by `type` field
4. **Response Streaming**: Send SSE events, end with `done`

```python
def handle():
    # 1. Auth check
    if request.headers.get("Authorization") != f"Bearer {KEY}":
        return {}, 401
    
    # 2. Type dispatch
    payload = request.get_json()
    if payload["type"] == "query":
        return stream_response()
    elif payload["type"] == "settings":
        return {"response_version": 1}
    else:
        return {}, 501

def stream_response():
    def stream():
        yield 'event: meta\ndata: {"content_type": "text/markdown"}\n\n'
        yield 'event: text\ndata: {"text": "Hello!"}\n\n'
        yield 'event: done\ndata: {}\n\n'
    return Response(stream(), mimetype="text/event-stream")
```

---

## 🔑 Important Details

### Request Types

| Type | When | Response |
|------|------|----------|
| `query` | User sends message | Stream SSE |
| `settings` | Bot config request | JSON |
| `report_reaction` | User reacts (heart) | 200 OK |
| `report_error` | Error occurred | 200 OK |

### Response Events (for query)

| Event | Purpose | Required |
|-------|---------|----------|
| `meta` | Configure (must be first) | ✅ |
| `text` | Response content | ✅ (≥1) |
| `suggested_reply` | Follow-up suggestions | ❌ |
| `file` | Attachment output | ❌ |
| `error` | Error occurred | ❌ |
| `done` | Complete response | ✅ |

### Limits

- **Initial response**: 5 seconds
- **Total response**: 3600 seconds (1 hour)
- **Max size**: 512,000 characters
- **Max events**: 10,000 per response

### Identifier Format

All IDs match pattern: `^[a-z]{1,3}-[a-z0-9=]{32}$`

- `m-` = message
- `u-` = user
- `c-` = conversation
- `d-` = metadata

---

## 🛠️ Common Patterns

### Error Response

```json
{
  "event": "error",
  "data": {
    "text": "User-friendly message",
    "allow_retry": true,
    "error_type": "user_caused_error"
  }
}
```

### File Attachment Output

```json
{
  "event": "file",
  "data": {
    "url": "https://...",
    "name": "output.pdf",
    "content_type": "application/pdf"
  }
}
```

### Suggested Replies

```json
{
  "event": "suggested_reply",
  "data": {"text": "Tell me more"}
}
```

---

## 🧪 Testing

### Basic Settings Test
```bash
curl -X POST http://localhost:5000 \
  -H "Authorization: Bearer key_here" \
  -H "Content-Type: application/json" \
  -d '{"type":"settings"}'
```

### Query Test
```bash
curl -X POST http://localhost:5000 \
  -H "Authorization: Bearer key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "query",
    "version": "1.0",
    "message_id": "m-a1234567890123456789012345678901",
    "user_id": "u-a1234567890123456789012345678901",
    "conversation_id": "c-a1234567890123456789012345678901",
    "query": [{"role": "user", "content": "hello"}]
  }'
```

---

## 💡 Pro Tips

1. **Use context managers** for streaming to ensure cleanup
2. **Validate input** - check for empty messages, reasonable length
3. **Set timeouts** - don't let external calls hang
4. **Stream progressively** - send partial updates for long responses
5. **Use `error` event** - not HTTP 500, stream the error as an event
6. **Test with curl** before deploying
7. **Log everything** - helpful for debugging
8. **Use HTTPS** in production
9. **Handle attachments** gracefully (check `parsed_content`)
10. **Return 501** for unknown request types (enables forward compatibility)

---

## 🔗 Related Resources

- **Poe Platform**: https://poe.com/
- **Server-Sent Events**: https://html.spec.whatwg.org/multipage/server-sent-events.html
- **GitHub-Flavored Markdown**: https://github.github.com/gfm/
- **Poe Python SDK**: https://github.com/poe-platform/poe-python-api

---

## 📖 Document Structure

```
docs/poe-protocol/
├── README.md                    (This file - overview)
├── POE_PROTOCOL_SPEC.md        (Complete specification)
├── QUICK_REFERENCE.md          (Cheat sheet)
└── IMPLEMENTATION_EXAMPLES.md  (7 working examples)
```

---

## 🚨 Common Mistakes

❌ **Forgot `done` event** - Response never completes  
❌ **`meta` not first** - May be ignored  
❌ **Returned 500 instead of `error` event** - Wrong pattern  
❌ **Took >5 seconds for first response** - Timeout  
❌ **Didn't verify Authorization** - Security issue  
❌ **JSON syntax errors in event data** - Parse failures  
❌ **Response >512KB** - Truncated by Poe  
❌ **Ignored unknown request types** - Breaks forward compatibility  

---

## 📞 Support

When troubleshooting:

1. Check the **QUICK_REFERENCE.md** checklists
2. Review similar example in **IMPLEMENTATION_EXAMPLES.md**
3. Check **POE_PROTOCOL_SPEC.md** limits and requirements
4. Test with curl - see if the bot responds correctly
5. Check server logs for errors
6. Verify Authorization header matches exactly
7. Ensure SSE format is correct (blank line after each event)

---

**Last Updated**: 2024  
**Protocol Version**: 1.0  
**Documentation Version**: 1.0

