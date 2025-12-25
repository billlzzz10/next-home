# Poe Protocol Implementation Examples

## 1. Echo Bot (Flask)

Simplest possible bot - echoes back user input.

```python
from flask import Flask, request, Response
import json

app = Flask(__name__)
ACCESS_KEY = "your_32_character_key_here_12345"

def send_event(event_type, data):
    """Helper to format SSE events"""
    return f"event: {event_type}\ndata: {json.dumps(data)}\n\n"

@app.route("/", methods=["POST"])
def handle():
    # Verify auth
    auth = request.headers.get("Authorization", "")
    if auth != f"Bearer {ACCESS_KEY}":
        return {"error": "Unauthorized"}, 401
    
    payload = request.get_json()
    request_type = payload.get("type")
    
    if request_type == "query":
        return handle_query(payload)
    elif request_type == "settings":
        return handle_settings()
    else:
        return {"error": "Not implemented"}, 501

def handle_query(payload):
    """Handle user message"""
    def stream():
        # Send metadata
        yield send_event("meta", {
            "content_type": "text/plain"
        })
        
        # Extract user message
        messages = payload.get("query", [])
        user_msg = messages[-1]["content"] if messages else "No message"
        
        # Echo it back
        yield send_event("text", {
            "text": f"You said: {user_msg}"
        })
        
        # Complete
        yield send_event("done", {})
    
    return Response(stream(), mimetype="text/event-stream")

def handle_settings():
    """Return bot configuration"""
    return {
        "response_version": 1,
        "introduction_message": "I echo back your messages!",
        "allow_attachments": False
    }

if __name__ == "__main__":
    app.run(debug=True, port=5000)
```

**Test:**
```bash
curl -X POST http://localhost:5000 \
  -H "Authorization: Bearer your_32_character_key_here_12345" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "query",
    "version": "1.0",
    "message_id": "m-a1234567890123456789012345678901",
    "user_id": "u-a1234567890123456789012345678901",
    "conversation_id": "c-a1234567890123456789012345678901",
    "query": [
      {"role": "user", "content": "Hello from Poe"}
    ]
  }'
```

---

## 2. Streaming Bot (FastAPI)

Streams response word-by-word with progress indicator.

```python
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import json
import asyncio

app = FastAPI()
ACCESS_KEY = "your_32_character_key_here_12345"

async def stream_response(text):
    """Stream text word by word"""
    words = text.split()
    
    # Meta event
    yield f'event: meta\ndata: {json.dumps({"content_type": "text/markdown"})}\n\n'
    
    # Stream text progressively
    current = ""
    for word in words:
        current += word + " "
        yield f'event: text\ndata: {json.dumps({"text": current})}\n\n'
        await asyncio.sleep(0.1)  # Simulate processing
    
    # Done
    yield f'event: done\ndata: {{}}\n\n'

@app.post("/")
async def handle(request: Request):
    # Auth check
    auth = request.headers.get("Authorization", "")
    if auth != f"Bearer {ACCESS_KEY}":
        return {"error": "Unauthorized"}, 401
    
    payload = await request.json()
    request_type = payload.get("type")
    
    if request_type == "query":
        # Extract user message
        messages = payload.get("query", [])
        user_msg = messages[-1]["content"] if messages else "Hello"
        
        response_text = f"You asked: {user_msg}\n\nThis is a streaming response demonstrating progressive output."
        
        return StreamingResponse(
            stream_response(response_text),
            media_type="text/event-stream"
        )
    
    elif request_type == "settings":
        return {
            "response_version": 1,
            "introduction_message": "I stream responses!"
        }
    
    else:
        return {"error": "Not implemented"}, 501
```

**Run:**
```bash
pip install fastapi uvicorn
uvicorn script:app --reload --port 5000
```

---

## 3. Calculator Bot

Parses mathematical expressions and returns results.

```python
from flask import Flask, request, Response
import json
import re

app = Flask(__name__)
ACCESS_KEY = "your_32_character_key_here_12345"

def send_event(event_type, data):
    return f"event: {event_type}\ndata: {json.dumps(data)}\n\n"

def calculate(expression):
    """Safely evaluate math expression"""
    try:
        # Only allow numbers, operators, parentheses
        if not re.match(r'^[\d+\-*/(). ]+$', expression):
            return None, "Invalid characters in expression"
        
        result = eval(expression)
        if isinstance(result, (int, float)):
            return result, None
        else:
            return None, "Invalid expression"
    except ZeroDivisionError:
        return None, "Division by zero"
    except Exception as e:
        return None, str(e)

@app.route("/", methods=["POST"])
def handle():
    auth = request.headers.get("Authorization", "")
    if auth != f"Bearer {ACCESS_KEY}":
        return {"error": "Unauthorized"}, 401
    
    payload = request.get_json()
    
    if payload.get("type") == "query":
        return handle_query(payload)
    elif payload.get("type") == "settings":
        return {
            "response_version": 1,
            "introduction_message": "Calculate: I evaluate math expressions"
        }
    else:
        return {"error": "Not implemented"}, 501

def handle_query(payload):
    def stream():
        yield send_event("meta", {"content_type": "text/markdown"})
        
        messages = payload.get("query", [])
        user_input = messages[-1]["content"] if messages else ""
        
        result, error = calculate(user_input)
        
        if error:
            response = f"❌ Error: {error}\n\nExpression: `{user_input}`"
        else:
            response = f"✅ Result: `{result}`\n\nExpression: `{user_input}`"
        
        yield send_event("text", {"text": response})
        yield send_event("done", {})
    
    return Response(stream(), mimetype="text/event-stream")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
```

---

## 4. Multi-Bot Orchestrator

Calls multiple other Poe bots and combines results.

```python
from flask import Flask, request, Response
import json
import requests

app = Flask(__name__)
ACCESS_KEY = "your_32_character_key_here_12345"

def send_event(event_type, data):
    return f"event: {event_type}\ndata: {json.dumps(data)}\n\n"

@app.route("/", methods=["POST"])
def handle():
    auth = request.headers.get("Authorization", "")
    if auth != f"Bearer {ACCESS_KEY}":
        return {"error": "Unauthorized"}, 401
    
    payload = request.get_json()
    
    if payload.get("type") == "query":
        return handle_query(payload)
    elif payload.get("type") == "settings":
        return {
            "response_version": 1,
            "introduction_message": "I coordinate multiple AI bots",
            "server_bot_dependencies": {
                "Claude": 1,
                "GPT-4": 1
            }
        }
    else:
        return {"error": "Not implemented"}, 501

def handle_query(payload):
    def stream():
        yield send_event("meta", {"content_type": "text/markdown"})
        
        messages = payload.get("query", [])
        user_msg = messages[-1]["content"] if messages else "Hi"
        
        # Header
        yield send_event("text", {
            "text": "# Multi-Bot Analysis\n\n"
        })
        
        # Bot 1
        yield send_event("text", {
            "text": "## Claude's Response\n"
        })
        yield send_event("text", {
            "text": f"*Analyzing: {user_msg}*\n\n"
        })
        yield send_event("text", {
            "text": "[Claude would respond here]\n\n"
        })
        
        # Bot 2
        yield send_event("text", {
            "text": "## GPT-4's Response\n"
        })
        yield send_event("text", {
            "text": f"*Analyzing: {user_msg}*\n\n"
        })
        yield send_event("text", {
            "text": "[GPT-4 would respond here]\n\n"
        })
        
        yield send_event("done", {})
    
    return Response(stream(), mimetype="text/event-stream")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
```

---

## 5. File Upload Handler

Accepts attachments and processes them.

```python
from flask import Flask, request, Response
import json
import requests
from urllib.parse import urlparse

app = Flask(__name__)
ACCESS_KEY = "your_32_character_key_here_12345"

def send_event(event_type, data):
    return f"event: {event_type}\ndata: {json.dumps(data)}\n\n"

@app.route("/", methods=["POST"])
def handle():
    auth = request.headers.get("Authorization", "")
    if auth != f"Bearer {ACCESS_KEY}":
        return {"error": "Unauthorized"}, 401
    
    payload = request.get_json()
    
    if payload.get("type") == "query":
        return handle_query(payload)
    elif payload.get("type") == "settings":
        return {
            "response_version": 1,
            "allow_attachments": True,
            "expand_text_attachments": True,
            "introduction_message": "Upload files to analyze"
        }
    else:
        return {"error": "Not implemented"}, 501

def handle_query(payload):
    def stream():
        yield send_event("meta", {"content_type": "text/markdown"})
        
        messages = payload.get("query", [])
        last_msg = messages[-1] if messages else {}
        
        attachments = last_msg.get("attachments", [])
        
        if not attachments:
            yield send_event("text", {
                "text": "No files attached. Please upload a file."
            })
        else:
            yield send_event("text", {
                "text": f"# Uploaded Files ({len(attachments)})\n\n"
            })
            
            for att in attachments:
                name = att.get("name", "unknown")
                content_type = att.get("content_type", "unknown")
                parsed = att.get("parsed_content", "")
                
                yield send_event("text", {
                    "text": f"## {name}\n"
                })
                yield send_event("text", {
                    "text": f"**Type**: {content_type}\n\n"
                })
                
                if parsed:
                    preview = parsed[:200] + "..." if len(parsed) > 200 else parsed
                    yield send_event("text", {
                        "text": f"**Content Preview**:\n```\n{preview}\n```\n\n"
                    })
        
        yield send_event("done", {})
    
    return Response(stream(), mimetype="text/event-stream")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
```

---

## 6. Error Handling Example

Demonstrates proper error handling and retries.

```python
from flask import Flask, request, Response
import json

app = Flask(__name__)
ACCESS_KEY = "your_32_character_key_here_12345"

def send_event(event_type, data):
    return f"event: {event_type}\ndata: {json.dumps(data)}\n\n"

@app.route("/", methods=["POST"])
def handle():
    auth = request.headers.get("Authorization", "")
    if auth != f"Bearer {ACCESS_KEY}":
        return {"error": "Unauthorized"}, 401
    
    payload = request.get_json()
    
    if payload.get("type") == "query":
        return handle_query(payload)
    elif payload.get("type") == "settings":
        return {
            "response_version": 1,
            "introduction_message": "I handle errors gracefully"
        }
    else:
        return {"error": "Not implemented"}, 501

def handle_query(payload):
    def stream():
        yield send_event("meta", {"content_type": "text/markdown"})
        
        try:
            messages = payload.get("query", [])
            user_msg = messages[-1]["content"] if messages else ""
            
            # Validate input
            if not user_msg.strip():
                yield send_event("error", {
                    "allow_retry": False,
                    "text": "Please provide some input",
                    "error_type": "user_caused_error"
                })
                yield send_event("done", {})
                return
            
            if len(user_msg) > 1000:
                yield send_event("error", {
                    "allow_retry": False,
                    "text": "Input too long (max 1000 characters)",
                    "error_type": "user_message_too_long"
                })
                yield send_event("done", {})
                return
            
            # Process
            yield send_event("text", {
                "text": f"Processed: {user_msg}"
            })
            
        except Exception as e:
            yield send_event("error", {
                "allow_retry": True,
                "text": f"Server error: {str(e)}",
                "error_type": "user_caused_error"
            })
        
        finally:
            yield send_event("done", {})
    
    return Response(stream(), mimetype="text/event-stream")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
```

---

## 7. Suggested Replies

Provides suggested follow-up questions.

```python
from flask import Flask, request, Response
import json

app = Flask(__name__)
ACCESS_KEY = "your_32_character_key_here_12345"

def send_event(event_type, data):
    return f"event: {event_type}\ndata: {json.dumps(data)}\n\n"

@app.route("/", methods=["POST"])
def handle():
    auth = request.headers.get("Authorization", "")
    if auth != f"Bearer {ACCESS_KEY}":
        return {"error": "Unauthorized"}, 401
    
    payload = request.get_json()
    
    if payload.get("type") == "query":
        return handle_query(payload)
    elif payload.get("type") == "settings":
        return {
            "response_version": 1,
            "introduction_message": "I suggest follow-up questions"
        }
    else:
        return {"error": "Not implemented"}, 501

def handle_query(payload):
    def stream():
        yield send_event("meta", {
            "content_type": "text/markdown",
            "suggested_replies": False  # We'll provide our own
        })
        
        messages = payload.get("query", [])
        user_msg = messages[-1]["content"] if messages else "Hi"
        
        yield send_event("text", {
            "text": f"You asked: {user_msg}\n\nHere's my response."
        })
        
        # Suggested follow-ups
        yield send_event("suggested_reply", {
            "text": "Tell me more"
        })
        yield send_event("suggested_reply", {
            "text": "Can you explain that differently?"
        })
        yield send_event("suggested_reply", {
            "text": "What's an example?"
        })
        
        yield send_event("done", {})
    
    return Response(stream(), mimetype="text/event-stream")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
```

---

## Testing These Examples

```bash
# Test any example with curl:
curl -X POST http://localhost:5000 \
  -H "Authorization: Bearer your_32_character_key_here_12345" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "query",
    "version": "1.0",
    "message_id": "m-a1234567890123456789012345678901",
    "user_id": "u-a1234567890123456789012345678901",
    "conversation_id": "c-a1234567890123456789012345678901",
    "query": [{"role": "user", "content": "test message"}]
  }' | head -20
```

