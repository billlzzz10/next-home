# Poe Protocol Specification

[Poe](https://poe.com/) is a platform for interacting with AI-based bots. This specification provides a way to run custom bots from any web-accessible service that integrates with Poe.

## Table of Contents

1. [Introduction](#introduction)
2. [Core Concepts](#core-concepts)
3. [Request Types](#request-types)
4. [Response Format](#response-format)
5. [Error Handling](#error-handling)
6. [Implementation Guide](#implementation-guide)

---

## Introduction

### Architecture

- **Poe Server**: Server run by Poe that receives client requests, transforms them into bot server requests, and streams responses back to Poe clients
- **Bot Server**: Server run by the creator that responds to requests from Poe servers. Responses are shown to users in their Poe client

### How It Works

1. User sends a message to a Poe bot in the Poe app
2. Poe server forwards this as an HTTP POST request to your bot server
3. Your bot server processes the request and sends back a stream of server-sent events
4. Poe streams the response back to the user in real-time

---

## Core Concepts

### Identifiers

Identifiers are globally unique, consisting of:
- 1-3 lowercase ASCII characters (tag representing object type)
- A hyphen `-`
- 32 lowercase alphanumeric ASCII characters or `=` characters

**Regex pattern**: `^[a-z]{1,3}-[a-z0-9=]{32}$`

**Types**:
- `m`: Message
- `u`: User
- `c`: Conversation (thread)
- `d`: Metadata sent with message

**Examples**:
```
m-a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
u-x1x2x3x4x5x6x7x8x9x0x1x2x3x4x5x6
c-abcdefghijklmnopqrstuvwxyz012345
d-metadata1234567890123456789012345
```

### Authentication

All requests include an `Authorization` HTTP header:
```
Authorization: Bearer <access_key>
```

The access key is 32 ASCII characters provided when creating the bot.

### Content Types

Messages support:
- `text/plain`: Plain text, no processing
- `text/markdown`: GitHub-Flavored Markdown (GFM)

### Versioning

Protocol version: `X.Y` where:
- **X (request version)**: Incremented for incompatible changes to the request format. Very rare.
- **Y (response version)**: Incremented when Poe adds new features bot servers can use. Backward-compatible.

**Key principle**: Bot servers should ignore any dictionary keys without specified meaning.

### Limits

- **Initial response**: Must return within 5 seconds
- **Total response time**: Must complete within 3600 seconds (1 hour)
- **Max response length**: 512,000 characters total
- **Max events**: 10,000 events per response
- **Conversation history**: Poe may truncate conversations exceeding 1000 messages

---

## Request Types

### 1. `query` Request

**When sent**: User sends a message to the bot

**Required fields**:

```json
{
  "version": "1.0",
  "type": "query",
  "query": [
    {
      "role": "system|user|bot",
      "content": "string",
      "content_type": "text/plain|text/markdown",
      "timestamp": 1234567890000000,
      "message_id": "m-xxxxx",
      "feedback": [
        {
          "type": "like|dislike",
          "reason": "optional reason"
        }
      ],
      "attachments": [
        {
          "url": "https://example.com/file.pdf",
          "content_type": "application/pdf",
          "name": "file.pdf",
          "parsed_content": "optional extracted text"
        }
      ],
      "parameters": {
        "key": "value"
      },
      "metadata": "optional metadata string"
    }
  ],
  "message_id": "m-xxxxx",
  "user_id": "u-xxxxx",
  "conversation_id": "c-xxxxx",
  "metadata": "d-xxxxx",
  "users": [
    {
      "id": "u-xxxxx",
      "name": "optional username"
    }
  ],
  "temperature": 0.7,
  "skip_system_prompt": false,
  "stop_sequences": ["\\n\\n", "---"],
  "logit_bias": {
    "token_id": 0.5
  }
}
```

**Message Roles**:
- `system`: System prompt/instructions
- `user`: User message
- `bot`: Bot response

**LLM Parameters** (optional, can be ignored):
- `temperature`: 0 (predictable) to ∞ (creative)
- `skip_system_prompt`: Minimize prompt engineering
- `stop_sequences`: Stop generation at these strings
- `logit_bias`: Adjust token probabilities

#### Response Format

Respond with HTTP 200 and `Content-Type: text/event-stream`.

Send server-sent events with format:
```
event: event_type
data: {"key": "value"}

```

**Event Types**:

| Event | Purpose | Data Keys |
|-------|---------|-----------|
| `meta` | Configuration (must be first) | `content_type`, `suggested_replies` |
| `text` | Response text (partial) | `text` |
| `file` | File attachment | `url`, `name`, `content_type`, `inline_ref` |
| `data` | Metadata (only last used) | `metadata` |
| `replace_response` | Replace previous text | `text` |
| `suggested_reply` | Suggested followup | `text` |
| `error` | Error occurred | `allow_retry`, `text`, `raw_response`, `error_type` |
| `done` | Response complete | (empty) |

**Meta Event Example**:
```json
{
  "event": "meta",
  "data": {
    "content_type": "text/markdown",
    "suggested_replies": true
  }
}
```

**Text Event Example**:
```json
{
  "event": "text",
  "data": {
    "text": "Hello, this is a response"
  }
}
```

**Minimal Valid Response**:
```
event: meta
data: {"content_type": "text/markdown"}

event: text
data: {"text": "Hello!"}

event: done
data: {}
```

---

### 2. `settings` Request

**When sent**: Poe queries bot configuration (initially and periodically)

**Request body**:
```json
{
  "version": "1.0",
  "type": "settings"
}
```

**Response**: HTTP 200 with `Content-Type: application/json`

```json
{
  "response_version": 1,
  "server_bot_dependencies": {
    "GPT-4": 1,
    "Claude": 2
  },
  "parameter_controls": {
    "api_version": "1.0",
    "sections": []
  },
  "allow_attachments": true,
  "expand_text_attachments": true,
  "enable_image_comprehension": false,
  "introduction_message": "Hello! I'm a helpful bot.",
  "enforce_author_role_alternation": false,
  "enable_multi_entity_prompting": false
}
```

**Settings Explained**:

| Setting | Type | Default | Purpose |
|---------|------|---------|---------|
| `response_version` | int | 0 | API version defaults |
| `server_bot_dependencies` | map | {} | Bots this bot calls (for tracking) |
| `parameter_controls` | object | - | UI controls for parameters |
| `allow_attachments` | bool | true | Accept file attachments |
| `expand_text_attachments` | bool | true | Parse text files |
| `enable_image_comprehension` | bool | false | Analyze images |
| `introduction_message` | string | "" | Greeting to user |
| `enforce_author_role_alternation` | bool | false | Enforce user/bot alternation |
| `enable_multi_entity_prompting` | bool | false | Multi-user prompting |

---

### 3. `report_feedback` Request (Deprecated)

**Replaced by**: `report_reaction`

---

### 4. `report_reaction` Request

**When sent**: User reacts to a message (heart, thumbs up, etc.)

**Request body**:
```json
{
  "version": "1.0",
  "type": "report_reaction",
  "message_id": "m-xxxxx",
  "user_id": "u-xxxxx",
  "conversation_id": "c-xxxxx",
  "reaction": "heart"
}
```

**Response**: HTTP 200 (content ignored)

---

### 5. `report_error` Request

**When sent**: Poe reports an error from your bot

**Request body**:
```json
{
  "version": "1.0",
  "type": "report_error",
  "message_id": "m-xxxxx",
  "conversation_id": "c-xxxxx",
  "error_message": "Connection timeout"
}
```

**Response**: HTTP 200 (content ignored)

---

## Response Format

### Server-Sent Events (SSE)

Follow the [WhatWG Server-Sent Events specification](https://html.spec.whatwg.org/multipage/server-sent-events.html).

**Format**:
```
event: type
data: {"json": "payload"}

event: type
data: {"json": "payload"}

```

**Key points**:
- Each event ends with blank line
- `data:` can be multi-line (indent continuation lines)
- Only the `data` field values are parsed as JSON

### Required Response Structure

**Minimum**:
```
event: meta
data: {"content_type": "text/markdown"}

event: text
data: {"text": "Response text"}

event: done
data: {}
```

**Complete Example**:
```
event: meta
data: {"content_type": "text/markdown", "suggested_replies": false}

event: text
data: {"text": "# Response\n\nThis is the first part."}

event: text
data: {"text": " This is appended."}

event: suggested_reply
data: {"text": "Tell me more"}

event: file
data: {"url": "https://example.com/output.pdf", "name": "output.pdf", "content_type": "application/pdf"}

event: done
data: {}
```

### Streaming Best Practices

1. **Send meta first**: Sets configuration for entire response
2. **Stream text progressively**: Send updates in chunks for long responses
3. **Add suggested replies**: Help users continue conversation
4. **File attachments**: Include after text content
5. **Metadata**: Use final `data` event to store state
6. **Always end with done**: Signals completion

---

## Error Handling

### Error Response Format

```json
{
  "event": "error",
  "data": {
    "allow_retry": true,
    "text": "User-friendly error message",
    "raw_response": null,
    "error_type": "user_caused_error"
  }
}
```

**Error Types**:

| Type | Meaning |
|------|---------|
| `insufficient_fund` | User out of compute points |
| `user_message_too_long` | Input exceeds limits |
| `user_caused_error` | Invalid input, unsupported format, etc. |

**HTTP Status Codes**:
- `200`: Success
- `400`: Bad request format
- `401`: Invalid authorization
- `500`: Server error
- `501`: Unknown request type (recommended for unsupported types)
- `503`: Service temporarily unavailable

---

## Implementation Guide

### Python Example: Flask Server

```python
from flask import Flask, request, jsonify, Response
import json
import os

app = Flask(__name__)
ACCESS_KEY = os.getenv("POE_ACCESS_KEY")

def verify_auth(req):
    """Verify Bearer token"""
    auth = req.headers.get("Authorization", "")
    expected = f"Bearer {ACCESS_KEY}"
    return auth == expected

def send_event(event_type, data):
    """Format SSE event"""
    return f"event: {event_type}\ndata: {json.dumps(data)}\n\n"

@app.route("/", methods=["POST"])
def handle_request():
    # Verify authentication
    if not verify_auth(request):
        return {"error": "Unauthorized"}, 401
    
    payload = request.get_json()
    request_type = payload.get("type")
    
    if request_type == "query":
        return handle_query(payload)
    elif request_type == "settings":
        return handle_settings()
    elif request_type == "report_reaction":
        return handle_reaction(payload)
    else:
        return {"error": "Unknown request type"}, 501

def handle_query(payload):
    """Process user query"""
    def stream():
        # Send metadata
        yield send_event("meta", {
            "content_type": "text/markdown",
            "suggested_replies": False
        })
        
        # Get user message
        messages = payload.get("query", [])
        user_message = messages[-1]["content"] if messages else ""
        
        # Process and send response
        yield send_event("text", {
            "text": f"You said: {user_message}"
        })
        
        # Send completion
        yield send_event("done", {})
    
    return Response(stream(), mimetype="text/event-stream")

def handle_settings():
    """Return bot settings"""
    return jsonify({
        "response_version": 1,
        "allow_attachments": True,
        "expand_text_attachments": True,
        "introduction_message": "Hello! How can I help?"
    })

def handle_reaction(payload):
    """Log user reaction"""
    message_id = payload.get("message_id")
    reaction = payload.get("reaction")
    print(f"User reacted {reaction} to message {message_id}")
    return {}, 200

if __name__ == "__main__":
    app.run(port=5000)
```

### Integration with Poe Python SDK

```python
from poe_python_api import Message, Chat

# When your bot receives a query request:
def process_query(query_payload):
    # Extract user message
    messages = query_payload["query"]
    user_msg = messages[-1]["content"]
    
    # Process
    response = f"Echo: {user_msg}"
    
    # Send events
    yield {
        "type": "meta",
        "data": {"content_type": "text/markdown"}
    }
    
    yield {
        "type": "text",
        "data": {"text": response}
    }
    
    yield {
        "type": "done",
        "data": {}
    }
```

### Testing Your Bot Server

```bash
# Test authentication
curl -X POST http://localhost:5000/ \
  -H "Authorization: Bearer invalid" \
  -H "Content-Type: application/json" \
  -d '{"type":"settings"}' 
# Should return 401

# Test settings
curl -X POST http://localhost:5000/ \
  -H "Authorization: Bearer YOUR_KEY_HERE" \
  -H "Content-Type: application/json" \
  -d '{"type":"settings"}' 
# Should return JSON settings

# Test query
curl -X POST http://localhost:5000/ \
  -H "Authorization: Bearer YOUR_KEY_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "query",
    "version": "1.0",
    "message_id": "m-test123456789012345678901234",
    "user_id": "u-test123456789012345678901234",
    "conversation_id": "c-test123456789012345678901234",
    "query": [{"role": "user", "content": "Hello"}]
  }' 
# Should stream SSE response
```

---

## Advanced Topics

### Accessing Other Poe Bots

If your bot calls other bots, declare them in settings:

```json
{
  "server_bot_dependencies": {
    "Claude": 1,
    "GPT-4": 2
  }
}
```

Pass the `metadata` field from the query request when calling other bots.

### Parameter Controls

Define interactive UI controls:

```json
{
  "parameter_controls": {
    "api_version": "1.0",
    "sections": [
      {
        "title": "Settings",
        "description": "Configure the bot",
        "controls": [
          {
            "type": "slider",
            "name": "temperature",
            "label": "Temperature",
            "min": 0,
            "max": 2,
            "step": 0.1,
            "default": 0.7
          }
        ]
      }
    ]
  }
}
```

### Handling Attachments

If `allow_attachments` is true:

1. Extract attachment URLs from `query` request
2. Fetch within 10 minutes (URL expires after)
3. If `expand_text_attachments` enabled, `parsed_content` field contains extracted text
4. If `enable_image_comprehension` enabled, `parsed_content` contains image description

```python
# In query handler
for attachment in payload["query"][0].get("attachments", []):
    url = attachment["url"]
    name = attachment["name"]
    parsed = attachment.get("parsed_content")
    
    # Use parsed_content if available
    if parsed:
        process_text(parsed)
```

### Metadata Persistence

Store state between requests using the `data` event:

```python
# Request 1: Store metadata
yield send_event("data", {"metadata": "state_value_123"})

# Request 2: Receive in query as payload["metadata"]
stored_state = payload["metadata"]
```

---

## Checklist: Deploy Your Bot

- [ ] Implement `/` endpoint accepting POST
- [ ] Verify `Authorization: Bearer` header
- [ ] Handle `query`, `settings`, `report_reaction` request types
- [ ] Stream SSE responses with `meta`, `text`, `done`
- [ ] Return within 5 seconds initially
- [ ] Complete response within 3600 seconds
- [ ] Keep response under 512,000 characters
- [ ] Test with curl or Postman
- [ ] Return 501 for unknown request types
- [ ] Handle attachments if enabled
- [ ] Log errors for debugging
- [ ] Use HTTPS in production
- [ ] Set appropriate timeouts
- [ ] Monitor bot performance

---

## Resources

- [Poe Platform](https://poe.com/)
- [Server-Sent Events Spec](https://html.spec.whatwg.org/multipage/server-sent-events.html)
- [GitHub-Flavored Markdown](https://github.github.com/gfm/)
- [poe-python-api](https://github.com/poe-platform/poe-python-api)

